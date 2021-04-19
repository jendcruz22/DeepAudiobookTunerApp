import os
import time


def path(relative_path):
    return os.path.abspath(relative_path)


def createDir(file_path):
    file_name = file_path.split("\\")[-1]
    file_name = file_name.split("/")[-1][:-4]
    creation_time = time.time()

    paths = {
        "audio_model": path(
            "../../assets/models/audio_sentiment_model/"
        ),
        "pickles": path("../../assets/pickles"),
        "text_model": path("../../assets/models/text_sentiment_model/"),
        "music_model": path(
            "../../assets/models/music_model/MusicTransformerKeyC.pth"
        ),
        "music_data": path("../../assets/pickles/"),
        "music_samples": path("../../assets/music_samples"),
        "wav_save_path": path(f"../../static/temp/{file_name}-{creation_time}"),
        "clips_save_path": path(f"../../static/temp/{file_name}-{creation_time}/clips"),
        "music_clips_save_path": path(
            f"../../static/temp/{file_name}-{creation_time}/music_clips"
        ),
        "final_audiobook_save_path": path(
            f"../../static/temp/{file_name}-{creation_time}/final_audiobook"
        ),
    }

    # Creating directories in temp to store the converted wav file and the clips
    os.mkdir(paths["wav_save_path"])
    os.mkdir(paths["clips_save_path"])
    os.mkdir(paths["music_clips_save_path"])
    os.mkdir(paths["final_audiobook_save_path"])

    print("----Temporary directory created.")

    return file_name, paths
