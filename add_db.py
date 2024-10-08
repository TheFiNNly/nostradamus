from create_db import User, SessionLocal
import parcing


def add_to_db(stats):
    add = User(champ=stats[0], date=stats[1], team_1=stats[2], team_1_goal=stats[3], team_1_xg=stats[6],
               team_1_corners=stats[8], team_1_fouls=stats[12], team_1_offside=stats[10], team_1_shots=stats[14],
               team_1_attacks=stats[16], team_1_possession=stats[18], team_1_red=stats[20], team_1_pass=stats[22],
               team_1_saves=stats[24], team_1_pass_acc=stats[26], team_1_tacking=stats[28], team_2=stats[4],
               team_2_goal=stats[5], team_2_xg=stats[7], team_2_corners=stats[9], team_2_fouls=stats[13],
               team_2_offside=stats[11], team_2_shots=stats[15], team_2_attacks=stats[17], team_2_possession=stats[19],
               team_2_red=stats[21], team_2_pass=stats[23], team_2_saves=stats[25], team_2_pass_acc=stats[27],
               team_2_tacking=stats[29])

    session = SessionLocal()
    session.add(add)
    session.commit()


teams = parcing.GetTeams().teams_table()
print(teams)

for team in teams:
    print(f'Парсим {team}')
    try:
        data = parcing.GetStats(team, 'NED1').regulator()
        print(f'Вносим в базу {team}')
        for match in data:
            add_to_db(match)
    except:
        print(f'Ошибка с {team}')

