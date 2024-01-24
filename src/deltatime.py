"""Deltatime retriever function"""
import time

def get_deltatime(previous_time:float=None) -> tuple[float, float] | float:
    """Get deltatime, used for pygame frametime independence

    :param previous_time: `time index`, defaults to None
    :type previous_time: float, optional
    :return: `(deltatime, new time index)` | `new time index`
    :rtype: tuple[float, float] | float
    """
    current_time = time.time()
    if previous_time:
        deltatime = current_time - previous_time
        return (deltatime, current_time)
    return current_time
