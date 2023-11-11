import aiohttp
import asyncio
import aiofiles

class Group:
    def __init__(self, groupid):
        self.groupid = groupid

    async def get_group_users(self, session):
        cursor = ''
        async with aiofiles.open(f"{self.groupid}.txt", "a+", encoding="utf-8") as file:
            while cursor != None:
                async with session.get(f"https://groups.roproxy.com/v1/groups/{self.groupid}/users?cursor={cursor}") as resp:
                        if resp.status == 429:
                            asyncio.sleep(60.0)
                            print("sleeping due to ratelimit for 60 secs")
                        else:
                            a = await resp.json() 
                            if('data' in a):
                                for user in a.get('data'):
                                    await file.write(str(user.get('user').get('userId')) + "\n")
                                cursor = a['nextPageCursor']        
        return file 

group = Group(input("enter group id: "))

async def main():
    async with aiohttp.ClientSession() as session:
        await group.get_group_users(session)
    print(f"done! saved result in {group.groupid}.txt")

asyncio.run(main())