from maa.context import SyncContext

# python -m pip install maafw
from maa.define import RectType
from maa.resource import Resource
from maa.controller import AdbController
from maa.instance import Instance
from maa.toolkit import Toolkit

from maa.custom_recognizer import CustomRecognizer
from maa.custom_action import CustomAction

import asyncio

async def main():
    user_path = "./"
    Toolkit.init_option(user_path)

    resource = Resource()
    await resource.load("assets/resource/mix")

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

    print("Start...")
    await maa_inst.run_task("OpenGame")
    await maa_inst.run_task("EnterGame")
    await maa_inst.run_task("StartSocial")
    await maa_inst.run_task("StartStore")
    await maa_inst.run_task("StartFracture")
    await maa_inst.run_task("StartEvent")
    await maa_inst.run_task("StartTask")
    await maa_inst.run_task("CloseGame")
    print("Finish")

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

        times_to_fight = 3

        self.fighting(context)

        print("Fight times: 1")

        for times_fight in range(times_to_fight - 1):
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

asyncio.run(main())