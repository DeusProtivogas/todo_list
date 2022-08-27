import os
from enum import Enum, unique, auto
from typing import Optional, Dict

from django.core.management import BaseCommand

from bot.tg.client import TgClient
from pydantic import BaseModel
from todolist import settings

from bot.tg.dc import Message

from bot.models import TgUser

from goals.models import Goal, GoalCategory



class NewGoal(BaseModel):
    cat_id: Optional[int] = None
    goal_title: Optional[str] = None

    def complete(self) -> bool:
        return None not in {self.cat_id, self.goal_title}

@unique
class StateEnum(Enum):
    CREATE_CATEGORY_STATE = auto()
    CHOSEN_CATEGORY = auto()

class FSMData(BaseModel):
    state: StateEnum
    goal: NewGoal

FSM_STATES: Dict[int, FSMData] = dict()
# FSM_STATES = dict()




class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    @staticmethod
    def _generate_verification_code() -> str:
        return os.urandom(12).hex()

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        code: str = self._generate_verification_code()
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"[verification code]: {code}",
        )

    def handle_goals_list(self, msg: Message, tg_user: TgUser):
        resp_goals: list[str] = [
            f'#{goal.id} {goal.title}'
            for goal in Goal.objects.filter(user_id=tg_user.user_id)
        ]
        self.tg_client.send_message(msg.chat.id, '\n'.join(resp_goals) or '[no goals found]')

    def handle_goal_cat_list(self, msg: Message, tg_user: TgUser):
        resp_cats: list[str] = [
            f'#{cat.id} {cat.title}'
            for cat in GoalCategory.objects.filter(
                board__participants__user_id=tg_user.user_id,
                is_deleted=False,
            )
        ]
        if resp_cats:
            self.tg_client.send_message(msg.chat.id, 'Select category\n{}'.format('\n'.join(resp_cats)))
        else:
            self.tg_client.send_message(msg.chat.id, 'No categories!')

    def handle_save_selected_category(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            cat_id = int(msg.text)
            if GoalCategory.objects.filter(
                board__participants__user_id=tg_user.user_id,
                is_deleted=False,
                id=cat_id,
            ).count():
                FSM_STATES[tg_user.chat_id].goal.cat_id = cat_id
                self.tg_client.send_message(msg.chat.id, '[set title]')
                FSM_STATES[tg_user.chat_id].state = StateEnum.CHOSEN_CATEGORY
                return
        self.tg_client.send_message(msg.chat.id, '[Invalid Category ID]')

    def handle_save_new_goal(self, msg: Message, tg_user: TgUser):
        goal: NewGoal = FSM_STATES[tg_user.chat_id].goal
        goal.goal_title = msg.text
        if goal.complete():
            Goal.objects.create(
                title=goal.goal_title,
                category_id=goal.cat_id,
                user_id=tg_user.user_id,
            )
            self.tg_client.send_message(msg.chat.id, text='[New Goal created]')
        else:
            self.tg_client.send_message(msg.chat.id, text='[Something went wrong]')

        FSM_STATES.pop(tg_user.chat_id, None)



    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if msg.text == '/goals':
            self.handle_goals_list(msg=msg, tg_user=tg_user)
        elif msg.text == '/create':
            self.handle_goal_cat_list(msg=msg, tg_user=tg_user)
            FSM_STATES[tg_user.chat_id] = FSMData(state=StateEnum.CREATE_CATEGORY_STATE, goal=NewGoal())

        elif msg.text == '/cancel' and tg_user.chat_id in FSM_STATES:
            FSM_STATES.pop(tg_user.chat_id)

        elif tg_user.chat_id in FSM_STATES:
            state: StateEnum = FSM_STATES[tg_user.chat_id].state
            if state == StateEnum.CREATE_CATEGORY_STATE:
                self.handle_save_selected_category(msg=msg, tg_user=tg_user)
            elif state == StateEnum.CHOSEN_CATEGORY:
                self.handle_save_new_goal(msg=msg, tg_user=tg_user)


        elif msg.text.startswith('/'):
            self.tg_client.send_message(msg.chat.id, '[incorrect command]')



    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=msg.chat.id,
            defaults={
                'username': msg.from_.username,
            }

        )
        if created:
            self.tg_client.send_message(msg.chat.id, '[hello]')
        elif not tg_user.user:
            self.handle_user_without_verification(msg=msg,tg_user=tg_user)
        else:
            self.handle_verified_user(msg=msg,tg_user=tg_user)



    def handle(self, *args, **options):
        offset = 0
        # tg_client = TgClient("token")

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(msg=item.message)
                # self.tg_client.send_message(chat_id=item.message.chat.id, text=item.message.text)

