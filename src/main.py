from config import config_client, config_task, config_event

from maa.context import SyncContext
from maa.define import RectType
from maa.resource import Resource
from maa.controller import AdbController
from maa.instance import Instance
from maa.toolkit import Toolkit
from maa.custom_action import CustomAction

import asyncio
import os

async def start():
    client_config = config_client()
    event_config = config_event()
    task_config = config_task()

    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def set_latest_event(event_config = config_event()):
        event_now = event_config.get_event_name_resource()
        print(f"The current event: {event_now}")
        event_to_set = input(f"Set the latest event (leave blank to continue using current activity):\n")
        if event_to_set:
            if event_config.config_event_name(event_to_set) and event_config.set_event(event_to_set):
                print(f"The current event set to: {event_to_set}")
            else:
                print(f"Setting failed, continue event {event_now}")
        return True

    def set_event_battle_time(event_config = config_event()):
        battle_time_now = event_config.get_event_time()
        print(f"The current battle times: {battle_time_now}")
        battle_time_to_set = input(f"Set battle times (leave blank to continue using current battle times):\n")
        if battle_time_to_set:
            if event_config.config_event_time(battle_time_to_set):
                print(f"The current battle times set to: {battle_time_to_set}")
            else:
                print(f"Setting failed, continue using battle times: {battle_time_now}")
        return True

    def add_task(task_config = config_task):
        clear()
        print("Current tasks: ")
        task_list = task_config.get_active_task_name()
        if task_list:
            for index, task in enumerate(task_list, start=1):
                print(f"\t{f'{index}.':4}{task}")
        print("Add task: ")
        task_list = task_config.get_task_names()
        for index, task in enumerate(task_list, start=1):
            print(f"\t{f'{index}.':4}{task}")
        add_task_index = int(input(f"Please input [1-{len(task_list)}]: "))
        task_config.add_task(add_task_index)
        return True

    def move_task(task_config = config_task):
        clear()
        print("Move task: ")
        task_list = task_config.get_active_task_name()
        if task_list:
            for index, task in enumerate(task_list, start=1):
                print(f"\t{f'{index}.':4}{task}")
            move_task_index = input(f"From [1-{len(task_list)}]: ")
            move_task_pos = input(f"To [1-{len(task_list)}]: ")
            task_config.move_task(move_task_index,move_task_pos)
        return True

    def delete_task(task_config = config_task()):
        clear()
        print("Delete task: ")
        task_list = task_config.get_active_task_name()
        if task_list:
            for index, task in enumerate(task_list, start=1):
                print(f"\t{f'{index}.':4}{task}")
            delete_task_index = int(input(f"Please input [1-{len(task_list)}]: "))
            task_config.remove_task(delete_task_index)
        return True

    async def main():
        # Initial Toolkit
        user_path = "./"
        Toolkit.init_option(user_path)

        # Connect ADB device
        device_list = await Toolkit.adb_devices()
        if not device_list:
            print("No ADB device found.")
            input("Press any key to exit...")
            exit()
        if len(device_list) == 1:
            device = device_list[0]
        else :
            print("Choose devices: ")
            device_index = 1
            for device in device_list:
                print(f"{device_index}. {device.address}")
                device_index += 1
            device_num = input(f"Please input [1-{len(device_list)}]: ")
            while int(device_num) not in range(1,len(device_list)+1):
                device_num = input(f"Invalid value, please input [1-{len(device_list)}]: ")
            device = device_list[int(device_num)-1]
        print(f"Connecting to controller: {device.address}...")
        controller = AdbController(
            adb_path=device.adb_path,
            address=device.address,
        )
        await controller.connect()
        print("Connected.")

        global times_to_fight
        event_name, times_to_fight = event_config.get_event()
        event_config.set_event(event_name)

        # Load resource
        resource = Resource()
        path = client_config.get_active_client_info()[1]
        await resource.load(path[0])

        print("Binding resource and controller...")
        maa_inst = Instance()
        maa_inst.bind(resource, controller)
        if not maa_inst.inited:
            print("Failed to init MAA.")
            input("Press any key to exit...")
            exit()
        print("Binded.")

        maa_inst.register_action("OpenGame", open_game)
        maa_inst.register_action("EnterGame", enter_game)
        maa_inst.register_action("StartSocial", start_social)
        maa_inst.register_action("StartStore", start_store)
        maa_inst.register_action("StartFracture", start_fracture)
        maa_inst.register_action("StartEvent", start_event)
        maa_inst.register_action("StartTask", start_task)
        maa_inst.register_action("FightStart", fight_start)
        maa_inst.register_action("FightEnd", fight_end)
        maa_inst.register_action("CloseGame", Close_game)

        entries = task_config.get_active_task_entry()
        for entry in entries:
            await maa_inst.run_task(entry)
        print("Finish")
        return True

    async def menu():
        while 1:
            clear()
            # Show current client
            print("Current client:")
            client_name, _ = client_config.get_active_client_info()
            print(f"\t{client_name}")

            # Show current tasks
            print("Tasks:")
            task_list = task_config.get_active_task_name()
            for index, task in enumerate(task_list, start=1):
                print(f"\t{f'{index}.':4}{task}")
            event_flag = 1 if 'StartEvent' in \
                task_config.get_active_task_entry() else 0

            # Show current event (if event task included)
            if event_flag:
                print("Current event:")
                print(f"\t{'Event name:':14}{event_config.get_event_name_resource()}")
                print(f"\t{'Battle times:':14}{event_config.get_event_time()}")

            # Select action
            print("### Select action ###")
            if event_flag:
                print(f"\t0. 配置活动 | Config event")
            print(f"\t1. 添加任务 | Add task")
            print(f"\t2. 移动任务 | Move task")
            print(f"\t3. 删除任务 | Delete task")
            print(f"\t4. 运行任务 | Run task")
            print(f"\t5. 退出程序 | Exit")

            action_index = int(input(f"Please input [{0 if event_flag else 1}-5]: "))
            while action_index not in range(0 if event_flag else 1,5+1):
                action_index = int(input(f"Invalid value, please input [{0 if event_flag else 1}-5]: "))

            if action_index == 0:
                clear()
                set_latest_event(event_config)
                set_event_battle_time(event_config)
            elif action_index == 1:
                add_task(task_config)
            elif action_index == 2:
                move_task(task_config)
            elif action_index == 3:
                delete_task(task_config)
            elif action_index == 4:
                await main()
            elif action_index == 5:
                os.system('cls' if os.name == 'nt' else 'clear')
                exit()

    await menu()

class OpenGame(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("StartGame")
        StartGame = context.run_task("StartGame")
        print(StartGame)

        print("ConfirmTerm")
        ConfirmTerm = context.run_task("ConfirmTerm")
        print(ConfirmTerm)

        print("GetUpdate")
        GetUpdate = context.run_task("GetUpdate")
        print(GetUpdate)

        print("DownloadResource")
        DownloadResource = context.run_task("DownloadResource")
        print(DownloadResource)

        print("WaitToEnter")
        WaitToEnter = context.run_task("WaitToEnter")
        print(WaitToEnter)

        return True

    def stop(self) -> None:
        pass

class EnterGame(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("ChooseServer")
        ChooseServer = context.run_task("ChooseServer")
        print(ChooseServer)

        print("EnterServer")
        EnterServer = context.run_task("EnterServer")
        print(EnterServer)

        print("DailyCheck-in")
        DailyCheck = context.run_task("DailyCheck-in")
        print(DailyCheck)

        print("SkipAnnouncement")
        SkipAnnouncement = context.run_task("SkipAnnouncement")
        print(SkipAnnouncement)

        while SkipAnnouncement:
            print("SkipAnnouncement")
            SkipAnnouncement = context.run_task("SkipAnnouncement")
            print(SkipAnnouncement)

        print("WaitForOtherTask")
        WaitForOtherTask = context.run_task("WaitForOtherTask")
        print(WaitForOtherTask)

        return True

    def stop(self) -> None:
        pass

class StartSocial(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("GotoSocial")
        GotoSocial = context.run_task("GotoSocial")
        print(GotoSocial)

        print("EnterMail")
        EnterMail = context.run_task("EnterMail")
        print(EnterMail)

        print("ReceiveMailReward")
        ReceiveMailReward = context.run_task("ReceiveMailReward")
        print(ReceiveMailReward)

        print("Back")
        Back_1 = context.run_task("Back")
        Back_2 = context.run_task("Back")
        print(Back_1 + Back_2)

        print("EnterClub")
        EnterClub = context.run_task("EnterClub")
        print(EnterClub)

        print("ReceiveClubReward")
        ReceiveClubReward = context.run_task("ReceiveClubReward")
        print(ReceiveClubReward)

        print("ReceiveClubRewardConfirm")
        ReceiveClubRewardConfirm = context.run_task("ReceiveClubRewardConfirm")
        print(ReceiveClubRewardConfirm)

        print("ResultConfirm")
        ResultConfirm = context.run_task("ResultConfirm")
        print(ResultConfirm)

        print("Back")
        Back = context.run_task("Back")
        print(Back)

        print("WaitForOtherTask")
        WaitForOtherTask = context.run_task("WaitForOtherTask")
        print(WaitForOtherTask)

        return True

    def stop(self) -> None:
        pass

class StartStore(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("GotoStore")
        GotoStore = context.run_task("GotoStore")
        print(GotoStore)

        print("EnterPackShop")
        EnterPackShop = context.run_task("EnterPackShop")
        print(EnterPackShop)

        print("ChooseHoumeiPack")
        ChooseHoumeiPack = context.run_task("ChooseHoumeiPack")
        print(ChooseHoumeiPack)

        print("FindGift_inverse")
        FindGift_inverse = context.run_task("FindGift_inverse")
        print(FindGift_inverse)

        while FindGift_inverse:
            print("SwipeDown")
            SwipeDown = context.run_task("SwipeDown")
            print(SwipeDown)

            print("FindGift_inverse")
            FindGift_inverse = context.run_task("FindGift_inverse")
            print(FindGift_inverse)

        print("ChooseGift")
        ChooseGift = context.run_task("ChooseGift")
        print(ChooseGift)

        print("BuyGift")
        BuyGift = context.run_task("BuyGift")
        print(BuyGift)

        print("ResultConfirm")
        ResultConfirm = context.run_task("ResultConfirm")
        print(ResultConfirm)

        print("Back")
        Back = context.run_task("Back")
        print(Back)

        print("WaitForOtherTask")
        WaitForOtherTask = context.run_task("WaitForOtherTask")
        print(WaitForOtherTask)

        return True

    def stop(self) -> None:
        pass

class StartFracture(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("GotoBattle")
        GotoBattle = context.run_task("GotoBattle")
        print(GotoBattle)

        print("BackToBattle")
        BackToBattle = context.run_task("BackToBattle")
        print(BackToBattle)

        while BackToBattle:
            print("BackToBattle")
            BackToBattle = context.run_task("BackToBattle")
            print(BackToBattle)

        print("FindFracture_inverse")
        FindFracture_inverse = context.run_task("FindFracture_inverse")
        print(FindFracture_inverse)

        while FindFracture_inverse:
            print("SwipeDown")
            SwipeDown = context.run_task("SwipeDown")
            print(SwipeDown)

            print("FindFracture_inverse")
            FindFracture_inverse = context.run_task("FindFracture_inverse")
            print(FindFracture_inverse)

        print("EnterFracture")
        EnterFracture = context.run_task("EnterFracture")
        print(EnterFracture)

        print("LoveOfServant")
        LoveOfServant = context.run_task("LoveOfServant")
        print(LoveOfServant)

        self.quick_fight(context)

        print("EnterVirtualCourt")
        EnterVirtualCourt = context.run_task("EnterVirtualCourt")
        print(EnterVirtualCourt)

        print("GotoFight")
        GotoFight = context.run_task("GotoFight")
        print(GotoFight)

        self.quick_fight(context)

        print("BackToBattle")
        BackToBattle = context.run_task("BackToBattle")
        print(BackToBattle)

        while BackToBattle:
            print("BackToBattle")
            BackToBattle = context.run_task("BackToBattle")
            print(BackToBattle)

        print("WaitForOtherTask")
        WaitForOtherTask = context.run_task("WaitForOtherTask")
        print(WaitForOtherTask)

        return True

    def quick_fight(self, context: SyncContext) -> bool:
        times_quick_fight = 0
        while True:
            print("QuickFight")
            QuickFight = context.run_task("QuickFight")
            print(QuickFight)

            if QuickFight:
                times_quick_fight += 1
                print("Quick fight times: ", times_quick_fight)
            else:
                print("Quick fight end.")

                print("Back")
                Back = context.run_task("Back")
                print(Back)

                return True

            print("QuickFightConfirm")
            QuickFightConfirm = context.run_task("QuickFightConfirm")
            print(QuickFightConfirm)

            print("ResultConfirm")
            ResultConfirm = context.run_task("ResultConfirm")
            print(ResultConfirm)

    def stop(self) -> None:
        pass

class StartEvent(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("GotoBattle")
        GotoBattle = context.run_task("GotoBattle")
        print(GotoBattle)

        print("BackToBattle")
        BackToBattle = context.run_task("BackToBattle")
        print(BackToBattle)

        while BackToBattle:
            print("BackToBattle")
            BackToBattle = context.run_task("BackToBattle")
            print(BackToBattle)

        print("FindEvent_inverse")
        FindEvent_inverse = context.run_task("FindEvent_inverse")
        print(FindEvent_inverse)

        while FindEvent_inverse:
            print("SwipeUp")
            SwipeUp = context.run_task("SwipeUp")
            print(SwipeUp)

            print("FindEvent_inverse")
            FindEvent_inverse = context.run_task("FindEvent_inverse")
            print(FindEvent_inverse)

        print("EnterEvent")
        EnterEvent = context.run_task("EnterEvent")
        print(EnterEvent)

        print("FindBONUS_inverse")
        FindBONUS_inverse = context.run_task("FindBONUS_inverse")
        print(FindBONUS_inverse)

        while FindBONUS_inverse:
            print("SwipeRight")
            SwipeRight = context.run_task("SwipeRight")
            print(SwipeRight)

            print("FindBONUS_inverse")
            FindBONUS_inverse = context.run_task("FindBONUS_inverse")
            print(FindBONUS_inverse)

        print("ChooseBONUS")
        ChooseBONUS = context.run_task("ChooseBONUS")
        print(ChooseBONUS)

        using_double = 1
        if using_double:
            print("UsingDouble")
            UsingDouble = context.run_task("UsingDouble")
            print(UsingDouble)

        print("ViewBuddyTable")
        ViewBuddyTable = context.run_task("ViewBuddyTable")
        print(ViewBuddyTable)

        self.fighting(context)

        print("Fight times: 1")

        for times_fight in range(int(times_to_fight) - 1):
            if using_double:
                print("UsingDouble")
                UsingDouble = context.run_task("UsingDouble")
                print(UsingDouble)

            print("FightAgain")
            FightAgain = context.run_task("FightAgain")
            print(FightAgain)

            self.fighting(context)

            print("Fight times: ", times_fight + 2)

        print("Fight Finished.")

        print("ResultConfirm")
        ResultConfirm = context.run_task("ResultConfirm")
        print(ResultConfirm)

        print("BackToBattle")
        BackToBattle = context.run_task("BackToBattle")
        print(BackToBattle)

        print("WaitForOtherTask")
        WaitForOtherTask = context.run_task("WaitForOtherTask")
        print(WaitForOtherTask)

        return True

    def fighting(self, context: SyncContext) -> bool:
        print("ChooseBuddy")
        ChooseBuddy = context.run_task("ChooseBuddy")
        print(ChooseBuddy)

        print("StartFight")
        StartFight = context.run_task("StartFight")
        print(StartFight)

        print("Fighting")
        Fighting = context.run_task("Fighting")
        print(Fighting)

        print("FightFinish")
        FightFinish = context.run_task("FightFinish")
        print(FightFinish)

    def stop(self) -> None:
        pass

class StartTask(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("GotoHome")
        GotoHome = context.run_task("GotoHome")
        print(GotoHome)

        print("EnterTask")
        EnterTask = context.run_task("EnterTask")
        print(EnterTask)

        print("GotoServantTravel")
        GotoServantTravel = context.run_task("GotoServantTravel")
        print(GotoServantTravel)

        print("ReceiveTravelReward")
        ReceiveTravelReward = context.run_task("ReceiveTravelReward")
        print(ReceiveTravelReward)

        while ReceiveTravelReward:
            print("Back")
            Back = context.run_task("Back")
            print(Back)

            print("ReceiveTravelReward")
            ReceiveTravelReward = context.run_task("ReceiveTravelReward")
            print(ReceiveTravelReward)

        print("ChooseServant")
        ChooseServant = context.run_task("ChooseServant")
        print(ChooseServant)

        while ChooseServant:
            print("QuickChoose")
            QuickChoose = context.run_task("QuickChoose")
            print(QuickChoose)

            print("StartTravel")
            StartTravel = context.run_task("StartTravel")
            print(StartTravel)

            print("ChooseServant")
            ChooseServant = context.run_task("ChooseServant")
            print(ChooseServant)

        print("GotoWeeklyTask")
        GotoWeeklyTask = context.run_task("GotoWeeklyTask")
        print(GotoWeeklyTask)

        print("QuickRecive")
        QuickRecive = context.run_task("QuickRecive")
        print(QuickRecive)

        if QuickRecive:
            print("Back")
            Back = context.run_task("Back")
            print(Back)

        print("GotoDailyTask")
        GotoDailyTask = context.run_task("GotoDailyTask")
        print(GotoDailyTask)

        print("QuickRecive")
        QuickRecive = context.run_task("QuickRecive")
        print(QuickRecive)

        if QuickRecive:
            print("Back")
            Back = context.run_task("Back")
            print(Back)

        print("Back")
        Back = context.run_task("Back")
        print(Back)

        print("WaitForOtherTask")
        WaitForOtherTask = context.run_task("WaitForOtherTask")
        print(WaitForOtherTask)

        return True

    def stop(self) -> None:
        pass

class FightStart(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("tap_down_1")
        tap_down_1 = context.touch_down(0, 320, 554, 1)
        print(tap_down_1)

        print("tap_down_2")
        tap_down_2 = context.touch_down(1, 1000, 630, 1)
        print(tap_down_2)

        return True

    def stop(self) -> None:
        pass

class FightEnd(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("tap_up_1")
        tap_up_1 = context.touch_up(0)
        print(tap_up_1)

        print("tap_up_2")
        tap_up_2 = context.touch_up(1)
        print(tap_up_2)

        return True

    def stop(self) -> None:
        pass

class CloseGame(CustomAction):
    def run(self, context, task_name, custom_param, box, rec_detail) -> bool:
        print("EndGame")
        EndGame = context.run_task("EndGame")
        print(EndGame)

        return True

    def stop(self) -> None:
        pass

open_game = OpenGame()
enter_game = EnterGame()
start_social = StartSocial()
start_store = StartStore()
start_fracture = StartFracture()
start_event = StartEvent()
start_task = StartTask()
fight_start = FightStart()
fight_end = FightEnd()
Close_game = CloseGame()

times_to_fight = 1

asyncio.run(start())