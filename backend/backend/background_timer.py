import asyncio


class CancellableTimer:
    def __init__(self, interval, callback, *args, **kwargs):
        """
        Initialize the timer.
        :param interval: Time in seconds for the timer to wait.
        :param callback: Coroutine function to execute after the interval.
        :param args: Positional arguments to pass to the callback.
        :param kwargs: Keyword arguments to pass to the callback.
        """
        self.interval = interval
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self._task = None

    async def _timer(self):
        try:
            await asyncio.sleep(self.interval)
            await self.callback(*self.args, **self.kwargs)
        except asyncio.CancelledError:
            raise Exception(
                "Timer was cancelled."
            )  # You can replace this with a custom exception or behavior.

    def start(self):
        """Start the timer as an asyncio task."""
        if self._task and not self._task.done():
            raise Exception("Timer is already running.")
        self._task = asyncio.create_task(self._timer())

    async def cancel(self):
        """Cancel the timer task."""
        if self._task:
            self._task.cancel()
            try:
                await self._task  # Wait for the task to handle the cancellation.
            except Exception as e:
                print(e)  # Handle or log the cancellation exception as needed.

    async def restart(self):
        """Restart the timer by cancelling and starting it again."""
        await self.cancel()
        self.start()
