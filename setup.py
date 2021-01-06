
from cx_Freeze import Executable, setup

executables = [Executable(script="2Cars.py", icon="CarsIcon2.ico"
                                    )]

setup(
    name="2Cars",
    options={"build_exe": {"packages":["pygame", "random", "math"],
                           "include_files":["2Cars Background Track MP3.mp3",
                                            "BlockL.png",
                                            "BlockR.png",
                                            "CarLF.png",
                                            "CarRF.png",
                                            "CircleL.png",
                                            "CircleR.png",
                                            "Collect.wav",
                                            "fire.png",
                                            "Hit.png",
                                            "Instructions.png",
                                            "KeyTap.wav",
                                            "Lose.png",
                                            "lostsound.wav",
                                            "MiniIcon.png",
                                            "Miss.png",
                                            "PenultimateLightItal_Regular.ttf",
                                            "Road.png",
                                            "RoadLines.png",
                                            "SEASRN_.ttf",
                                            "Start.png",
                                            "CarsIcon2.ico"
                                            ]}},
    executables = executables

    )