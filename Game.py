#Gears Of War: Turn-Based Combat!

from random import randint
from time import sleep
from sys import exit

Characters = { "COG": ["MARCUS" ,"DOM", "BAIRD", "COLE", "CARMINE", "KEZDREW"], "LOCUST": ["MYRRAH", "THERON", "DRONE", "GRENADIER", "SKORGE", "RAAM"]}
Character_Health = {"MARCUS": 80, "DOM": 2, "BAIRD": 70, "COLE": 100, "CARMINE": 60, "KEZDREW": 100, "MYRRAH": 90, "THERON": 70, "DRONE": 50, "GRENADIER": 70, "SKORGE": 85, "RAAM": 90}
Character_Attack = {"MARCUS": 4, "DOM": 4, "BAIRD": 3, "COLE": 5, "CARMINE": 3, "KEZDREW": 3, "MYRRAH": 3, "THERON": 4, "DRONE": 3, "GRENADIER": 4, "SKORGE": 5, "RAAM": 4}
Character_weapons = {"MARCUS": ["frag", "lancer", "chainsaw"], "DOM": ["frag", "gnasher"], "BAIRD": ["longshot"], "COLE": ["frag", "boomshot", "boltok"], "CARMINE": ["frag", "lancer", "chainsaw"], "KEZDREW": ["chainsaw", "ink", "gnasher"],
                     "MYRRAH": ["frag", "gorgon"], "THERON": ["torque bow", "gorgon"], "DRONE": ["frag", "hammerburst"], "GRENADIER": ["frag", "gnasher"], "SKORGE": ["gorgon", "ink", "chainsaw"], "RAAM": ["frag","boltok"]}



#list of characters that the users uses as their 'team'
Selected_Characters = {"COG": [], "LOCUST": []}

#weapon_damage[x][0] = weapon x's lower damage, weapon_damage[x][1] = weapon x's upper damage
#value of weapon_damage[i][j] affects the health reduction on a victim.
weapon_damage = {"frag": [5, 7], "gorgon": [2, 3], "lancer": [2, 3], "gnasher": [4, 5], "hammerburst": [2, 4], "boomshot": [6, 7], "longshot": [4, 5], "boltok": [3, 4], "ink": [0,0], "torque bow": [5, 7]}
faction_turn = "LOCUST"
next_turn_faction = "COG"

def main():


    def explosive_attack():

        if weapon == "frag":
            print(attacker, "Throwing ", weapon, "!")
        elif weapon == "boomshot":
            print("BOOOOOM BABY!")
        elif weapon == "torque bow":
            print("HOSTILES!!")  # theron trademark line
        sleep(1)
        missed = randint(1, 2)
        if missed == 2:
            print(attacker, "missed!")
            weapon = ""
        else:
            # ink grenade deals damage over time, as the victim continues to breath in the poison
            if weapon == "ink":
                for i in range(1, randint(2, 5)):
                    Character_Health[victim] -= 3 * i
                    get_player_health(victim)
                    sleep(.5)
                print("")
                weapon = ""
        return weapon

    def chainsaw_attack():

        success = randint(1, 7)
        if success > Character_Attack[attacker]:
            print("The attack was unsuccessful")
            Character_Health[attacker] -= 10 * randint(2, 3)
            get_player_health(attacker)
        else:
            # ..and even if they get a chance to reach the victim, they could be met with the very same weapon...
            if victim in ["SKORGE", "CARMINE", "MARCUS"]:
                attacker_fight = randint(1, 5) * Character_Attack[attacker]
                victim_fight = randint(1, 5) * Character_Attack[victim]
                sleep(1)
                if attacker_fight == victim_fight:
                    print("It's a draw")
                elif victim_fight > attacker_fight:
                    Character_Health[victim] -= 5 * randint(1, 4)
                    Character_Health[attacker] = 0
                    print(attacker, "got chainsawed")
            else:
                # ..or the victim could be hopeless and reach an inevitable death
                Character_Health[attacker] -= 5 * randint(1, 4)
                Character_Health[victim] = 0
                print(victim, "got chainsawed")
                get_player_health(attacker)
        weapon = "" # returns empty string to show that attack has already been completed.
        return weapon

    def cole_frenzy():

        sleep(1)
        print("Cole: NUMBER 83, THE COLE TRAIN!!")
        sleep(1)
        print("Cole has gone into a melee frenzy!")
        Character_Health[victim] -= Character_Attack[attacker] * randint(2, 3)
        Character_Health[attacker] -= Character_Attack[victim] * randint(1, 2)
        get_player_health(attacker)


    def suicide():

        Character_Health[attacker] = 0
        if attacker == "DOM":
            # Dom has the chance to kill both his victim and himself
            print("Dom goes suicidal, blowing himself and", victim, "to pieces!")
            Character_Health[victim] = 0
        else:
            print("Cole blew himself up!")

#where damage is calculated....
    def damage(attacker, victim, weapon):

        #there is a slim chance that if the attacker is Cole, then he will have his own special attack
        if weapon == "Cole frenzy":
            cole_frenzy()
        elif weapon == "suicide":
            suicide()


        else:
            print(attacker, " attacks ", victim, " with ", weapon)


            #A chainsaw attack is risky, there is a chance to battle is too hot and the attacker has to back out of the attack...
            if weapon == "chainsaw":

                chainsaw_attack()


            #explosives and thrown weapons have a chance of msissing
            if weapon in ["ink", "frag", "boomshot", "torque bow"]:

                explosive_attack()

            # some weapons are so strong they can insta kill their victims
            if weapon in ["longshot", "boltok", "torque bow", "frag", "boomshot"]:
                insta_kill_chance = randint(1, 10)
                if insta_kill_chance == 1:
                    Character_Health[victim] = 0
                    death = "headshot"
                    if weapon == "torque bow":
                        death = "torque bow tagged"
                    elif weapon != "longahot":
                        death = "blew up"
                    print(attacker, death, victim)
                    weapon = ""
            if weapon != "" and weapon != "suicide":
                Character_Health[victim] -= Character_Attack[attacker]*(randint(weapon_damage[weapon][0], weapon_damage[weapon][1]))
        if weapon != "suicide":
            get_player_health(victim)
        attack()


# when choosing a weapon, the user is presented with a numbered list of options, to which they will need to enter exactly that number otherwise he will continue to ask
    def weapon_select(weapon_list, dom):

        selected_weapon = ""
        weapon_display = ""
        for i in range(0, len(weapon_list)):
            weapon_display = weapon_display + weapon_list[i] + ": " + str(i+1) + " "
        while True:
            try:
                weapon = int(input(weapon_display)) - 1
                if weapon >= 0 and weapon < len(weapon_list) :
                    selected_weapon = weapon_list[weapon]
                    break
                else:
                    print("invalid selection")
            except ValueError:
                print ("invalid choice")

        # Dom + frag = risky move, also Boomshots are dangerous
        if (weapon_list[weapon] == "frag" and dom == True) or weapon_list[weapon] == "boomshot":
            suicide = randint(1,10)
            if suicide == 1:
                selected_weapon = "suicide"
        return selected_weapon


#when selecting a character, cog selects their team first, then locust
    def characters_select():

        chosen_cog = []
        chosen_locust = []

        faction_lists = {"COG": chosen_cog, "LOCUST": chosen_locust}

        characters_selected = 0

        #3 per team
        while characters_selected < 6:

                faction_selecting = "COG"
                faction_dict = chosen_cog
                if characters_selected > 2:
                    faction_selecting = "LOCUST"
                    faction_dict = chosen_locust
                character_chosen = input("Choose a " + faction_selecting).upper()
                characters_selected += 1

                #the user must type the name exactly how it is spelt, case is irrelevant, it must also be in the team that is currently being selected.
                if character_chosen in Characters.get(faction_selecting) and character_chosen not in faction_dict:
                    Selected_Characters[faction_selecting].append(character_chosen)
                    faction_lists[faction_selecting].append(character_chosen)
                else:
                    print ("invalid selection")
                    characters_selected = len(chosen_cog) + len(chosen_locust)
    #Myrrah in the same team as the Drone makes them stronger
        if "DRONE" in chosen_locust and "MYRRAH" in chosen_locust:
            print ("correct")
            Character_Attack["DRONE"] = 5
        print (" ".join(chosen_cog), "vs"," ".join(chosen_locust))


    def attack():

        global faction_turn
        global next_turn_faction

        display_teams()


        attacker = get_character(faction_turn, faction_turn, "attacker")
        victim = get_character(next_turn_faction, faction_turn, "victim")

        print (attacker, "attacks", victim)

        if faction_turn == "LOCUST":
            faction_turn = "COG"
            next_turn_faction = "LOCUST"
        else:
            faction_turn = "LOCUST"
            next_turn_faction = "COG"
        print("")
        dom = False
        if attacker == "DOM":
            dom = True
        if attacker == "BAIRD":
            damage(attacker, victim, "longshot")
        else:
            damage(attacker, victim, weapon_select(Character_weapons[attacker], dom))

#depending on who's turn it is, they must type the name of the character to fight. must match from those that they selected
    def get_character(faction, faction_turn, subject):
        # subject = "attacker" | "victim"

        faction_list = Selected_Characters[faction]
    #if theres only one player left on a team they are selected automatically.
        if len(faction_list) == 1:
            character =  faction_list[0]
        else:
            while True:
                try:
                    character = input(faction_turn + ": Choose your " + subject).upper()
                    if character in Selected_Characters[faction]:
                        break
                    else:
                        print ("invalid ", subject)
                except ValueError:
                    print("invalid input")
        print(character, " selected")
        return character


    #after each attack, the teams are shown with updated health values, those who are dead are not shown
    #although if one team has no more players, then the game ends. A draw is also possible.
    def display_teams():
            print ("")
            get_team_health("COG")
            print("")
            get_team_health("LOCUST")

            locust_left = len(Selected_Characters["LOCUST"])
            cog_left = len(Selected_Characters["COG"])
            total_left = locust_left + cog_left
            if total_left == 0:
                print("it's a draw")
                exit()
            elif cog_left == 0:
                print("Locust win!")
                exit()
            elif locust_left == 0:
                print("COG win!")
                exit()

    def get_team_health(faction):
        for thing in Selected_Characters[faction] :
            print (thing, " health: ", Character_Health[thing])


    def get_player_health(player):

        character_health = Character_Health[player]

        if character_health < 0:
            character_health = 0
            # players who have <= 0 health are removed from their respective Selected_Characters list
            if Selected_Characters["COG"].__contains__(player):
                Selected_Characters["COG"].remove(player)

            elif Selected_Characters["LOCUST"].__contains__(player):
                Selected_Characters["LOCUST"].remove(player)

        return print(player + "'s health is now", character_health)

    characters_select()
    attack()
if __name__ == '__main__':
    main()