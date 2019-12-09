
class MyModule:
    async def say_hello(self):
        some_string = "world"
        # f-strings do not work
        # await self.chat_send(f"Hello {some_string}")
        # print(f"Hello {some_string}")
        await self.chat_send("Hello {}".format(some_string))
        print("Hello {}".format(some_string))

