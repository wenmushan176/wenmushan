import random

def get_computer_choice():
    return random.choice(['石头', '剪刀', '布'])

def get_player_choice():
    choice = input("请输入你的选择（石头、剪刀、布）：")
    while choice not in ['石头', '剪刀', '布']:
        choice = input("无效的选择，请重新输入：")
    return choice

def determine_winner(player, computer):
    if player == computer:
        return "平局"
    elif (player == '石头' and computer == '剪刀') or \
         (player == '剪刀' and computer == '布') or \
         (player == '布' and computer == '石头'):
        return "玩家赢"
    else:
        return "计算机赢"

def play_game():
    while True:
        computer_choice = get_computer_choice()
        player_choice = get_player_choice()
        print(f"计算机选择了：{computer_choice}")
        result = determine_winner(player_choice, computer_choice)
        print(result)
        if input("是否继续游戏？(是/否): ") != '是':
            break

play_game()