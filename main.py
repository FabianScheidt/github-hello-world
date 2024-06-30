from datetime import datetime, timezone, timedelta
import subprocess
from typing import List

import cv2
import numpy as np


def read_img(img_src: str) -> np.ndarray:
    img = cv2.imread(img_src, cv2.IMREAD_GRAYSCALE)
    return img < 127


def get_dates(img: np.ndarray, year: int) -> List[datetime]:
    assert img.shape == (7, 51), "Expected input array to have shape (7, 51): 51 full weeks, 7 days each"
    assert img.dtype == bool, "Expected input array to have dtype bool"
    img_list = img.reshape((7 * 51), order="F").tolist()

    # Start on first Sunday of the year
    next_date = datetime(year=year, month=1, day=1, hour=12, tzinfo=timezone.utc)
    while next_date.weekday() != 6:
        next_date += timedelta(days=1)

    # Iterate img_list
    dates = []
    for el in img_list:
        if el:
            dates.append(next_date)
        next_date += timedelta(days=1)

    return dates


def commit_date(date: datetime, message: str):
    date_str = date.isoformat()
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", message],
        env={
            "GIT_AUTHOR_DATE": date_str,
            "GIT_COMMITTER_DATE": date_str,
        }
    )


if __name__ == '__main__':
    hello_world_img = read_img("./hello-world.png")
    hello_world_dates = get_dates(hello_world_img, 1993)
    for hello_world_date in hello_world_dates:
        commit_date(hello_world_date, "chore: add hello-world commit")
