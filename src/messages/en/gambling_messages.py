def user_can_not_pay(user_mention: str, balance: int):
    msg = f'''
🎩 **Yikes, {user_mention}!** 🎩

You’re flat broke, kiddo! Can’t make it rain without the dough. 💸  
Your current balance is **{balance} coins** :moneybag:.  

*"Better get back to work, champ—those coins won’t earn themselves!"* 😅
        '''
    return msg


def flip_reward_message(user_mention: str, value: int):
    msg = f'''
🎉 **Hot diggity dog, {user_mention}!** 🎉

You hit the jackpot! 🎰  
**{value} coins** are now yours to keep! :money_mouth:  

*"Keep throwing those coin, big shot—you’re on a winning streak!"* 🤑
        '''
    return msg


def flip_loss_message(user_mention: str, value: int):
    msg = f'''
💔 **Oh no, {user_mention}!** 💔

The house always wins, kiddo. 🎰  
**{value} coins** just flew outta your pocket! :money_with_wings:  
        '''
    return msg
