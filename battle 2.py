import random
import os

#dictionary :3

correct = ["Yes", "yes", "y"]
incorrect = ["No", "no", "n"]
fight = ["A", "a"]
check = ["C", "c"]
heal = ["H", "h"]

#type ideas: fire (FIR), water (WTR), grass (GRS), thunder (THN), ice (ICE), poison (POI), sharp (SRP), blunt (BNT)

#status vvv

#burnt (BRN) (sharp and blunt down, 1/16 damage per turn), soggy (SOG) (fire down, more damage from water/thunder)

#tangled (TGL) (blunt and thunder down, speed halved), shocked (SHK) (more damage from thunder, when hit by thunder do 2nd attack at 1/3 damage)

#frozen (FRZ) (water, grass, poison down, cannot move 50%), poisoned (PSN) (sharp up, blunt down, more from poison 1/16 damage every turn)

#silly (SIL) silly (SIL) (sharp down poison down, spd x 2)

#fire: incinerate (1.2 x atk 30% burn), explosion (1/2 max health, 1.8 x atk 50% burn), roast (0.6 x atk 100% burn)
#water: flood (1.2 x atk 30% soggy), whirlpool (0.7 x atk twice 25% soggy), rehydrate (0.5 x atk, heal 1/3 damage you deal, 100% soggy)
#grass: 
#thunder: 
#ice:
#poison:
#sharp: 
#blunt: 
#silly:

class types:
    def __init__(types, type, t_status):
        types.type = type
        types.t_status = t_status
    def __str__(types):
        return f"{types.type}"
        pass
class status_:
    def __init__(status, s_name):
        status.s_name = s_name
    def __str__(status):
        return f"{status.s_name}"
        pass

BRN = status_("Burnt")
FIR = types("Fire", BRN)
SOG = status_("Soggy")
WTR = types("Water", SOG)
TGL = status_("Tangled")
GRS = types("Grass", TGL)
SHK = status_("Shocked")
THN = types("Thunder", SHK)
FRZ = status_("Frozen")
ICE = types("Ice", FRZ)
PSN = status_("Poisoned")
POI = types("Poison", PSN)
SRP = types("Sharp", "")
BNT = types("Blunt", "")
SILLY = status_("Silly")
SIL = types("Silly", SILLY)

class moveset:
    def __init__(self, move1, move2, move3, move4):
        self.move1 = move1
        self.move2 = move2
        self.move3 = move3
        self.move4 = move4
    
    def has_moves(self):
        return self.move1 in moveset

    def display_moves(self):
        print(f"{self.move1}"   f"{self.move2}"
              f"                    "
              f"{self.move3}"   f"{self.move4}")
        pass
class move:
    def __init__(attack, atk_name, type, power, status_chance, status_chance_dec):
        attack.atk_name = atk_name
        attack.type = type
        attack.power = power
        attack.status_chance = status_chance
        attack.status_chance_dec = status_chance_dec
    def __str__(attack):
        return f"{attack.atk_name} {attack.type}, Power: Atk x {attack.power} Effects: {attack.status_chance_dec}"
        pass
    def __str__(self):
        return f"{self.atk_name}, Type: {self.type}, Power: Atk x {self.power}, Effects: {self.status_chance_dec}"
        pass
        pass


class HealthBar:
    symbol_remaining: str = "█"
    symbol_lost: str = "_"
    barrier: str = "|"
    colors: dict = {"red": "\033[91m", 
                    "green": "\033[32m"}

    def __init__(self,
                 entity, 
                 length: int = 20, 
                 is_colored: bool = True, 
                 color: str = "") -> None:
        self.entity = entity
        self.length = length
        self.max_value = entity.hp_max
        self.current_value = entity.hp

        self.is_colored = is_colored
        self.color = self.colors.get(color) or self.colors["red"]
    
    def update(self) -> None:
        self.current_value = self.entity.hp
    
    def draw(self) -> None:
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        print(f"{self.entity.name}'s HEALTH: {self.entity.hp}/{self.entity.hp_max}")
        print(f"{self.barrier}"
              f"{self.color if self.is_colored else ""}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors["red"] if self.is_colored else ""}"
              f"{self.barrier}")
        pass

class me:
    def __init__(self, name, lvl, hp, atk, defn, spd, exp, exp_tonext):
        
        self.name = name
        self.lvl = lvl
        self.hp = hp
        self.hp_max = hp
        self.atk = atk
        self.defn = defn
        self.spd = spd
        self.exp = exp
        self.exp_tonext = exp_tonext
        self.status = []
        self.strength = []
        self.weakness = []
        self.health_bar = HealthBar(self, color="green")
        pass
    def add_status(self, status):
        if status not in self.status:
            self.status.append(status)
    
    def remove_status(self, status):
        if status in self.status:
            self.status.remove(status)
    
    def has_status(self, status):
        return status in self.status
    
    def display_status(self):
        print(f"{self.name} is {', '.join(self.status)}")
    
    def status_effect(self):
        if self.status == BRN:
            self.hp -= ((1/16)*self.hp)
            self.weakness.append(FIR)
        elif self.status == SOG:
            self.weakness.append(THN, WTR)
        elif self.status == TGL:
            self.spd = ((1/2)*self.spd)
            self.weakness.append(GRS, POI)
        elif self.status == SHK:
            self.defn -= ((1/2)*self.defn)
            self.weakness.append(THN)
        elif self.status == FRZ:
            self.atk == ((1/2)*self.atk)
            self.weakness.append(ICE)
        elif self.status == PSN:
            self.hp -= ((1/8)*self.hp)
            self.strength.append(SRP)
            self.weakness.append(POI)
        elif self.status == SILLY:
            self.atk = ((1.2)*self.atk)
            self.weakness.append(SRP, POI)
            self.strength.append(SIL)
    
    def attack(self, target) -> None:
        target.hp -= damage
        damage = (((((2 * self.lvl)/5)+2) * ((self.atk)/(target.defn))/50)+2) * self.strength * target.weakness * random.randrange(0.85, 1)
        target.hp = max(target.hp, 0)
        target.health_bar.update()
        print(f"{self.name} dealt {damage} damage to"
              f"{target.name}!")
    
    def me_moveset(self, 
                   move1, 
                   move2, 
                   move3, 
                   move4):
        self.move1 = move1
        self.move2 = move2
        self.move3 = move3
        self.move4 = move4 

    def me_has_moves(self):
        return me.me_moveset(self)

    def display_moves(self):
        print("\n" + "=" * 30)
        print(f"ATTACK!!")
        print("=" * 30)
        print(f"1. {self.move1}\n2. {self.move2}\n3. {self.move3}\n4. {self.move4}")
        print("=" * 30)

    
class evil:
    def __init__(enemy, name, lvl, hp, atk, defn, spd, exp_give, type):
        
        enemy.name = name
        enemy.lvl = lvl
        enemy.hp = hp
        enemy.hp_max = hp
        enemy.atk = atk
        enemy.defn = defn
        enemy.spd = spd
        enemy.exp_give = exp_give
        enemy.type = type
        enemy.status = []
        enemy.strength = []
        enemy.weakness = []
        enemy.health_bar = HealthBar(enemy, color="red")
        pass
    def add_status(enemy, status):
        if status not in enemy.status:
            enemy.status.append(status)
    
    def remove_status(enemy, status):
        if status in enemy.status:
            enemy.status.remove(status)
    
    def has_status(enemy, status):
        return status in enemy.status
    
    def display_status(enemy):
        print(f"{enemy.name} is {', '.join(enemy.status)}")
    
    def status_effect(enemy):
        if enemy.status == BRN:
            enemy.hp -= ((1/16)*enemy.hp)
            enemy.weakness.append(FIR)
        elif enemy.status == SOG:
            enemy.weakness.append(THN, WTR)
        elif enemy.status == TGL:
            enemy.spd = ((1/2)*enemy.spd)
            enemy.weakness.append(GRS, POI)
        elif enemy.status == SHK:
            enemy.defn -= ((1/2)*enemy.defn)
            enemy.weakness.append(THN)
        elif enemy.status == FRZ:
            enemy.atk == ((1/2)*enemy.atk)
            enemy.weakness.append(ICE)
        elif enemy.status == PSN:
            enemy.hp -= ((1/8)*enemy.hp)
            enemy.strength.append(SRP)
            enemy.weakness.append(POI)
        elif enemy.status == SILLY:
            enemy.atk = ((1.2)*enemy.atk)
            enemy.weakness.append(SRP, POI)
            enemy.strength.append(SIL)
    
    def attack(enemy) -> None:
        player.hp -= damage
        damage = (((((2 * enemy.lvl)/5)+2) * ((enemy.atk)/(enemy.defn))/50)+2) * enemy.strength * player.weakness * random.randrange(0.85, 1)
        player.hp = max(player.hp, 0)
        player.health_bar.update()
        print(f"{enemy.name} dealt {damage} damage to"
              f"{player.name}!")
    pass

e_list = ["Femboy", "Boykisser", "Serial Killer"]

mobs = {
    evil("Femboy", 10, 20, 10, 10, 9, 9, SIL), 
    evil("Boykisser", 10, 20, 10, 10, 9, 9, SIL), 
    evil("Serial Killer", 10, 20, 10, 10, 9, 9, SIL)
}

incin = move("Incinerate", FIR, 1.2, random.randint(0, 2), "33% burn")
shit_pants = move("shit pants", WTR, 2, random.randint(0, 0), "100% soggy, shits pants :(") 
meow = move("Meow", SIL, 0.5, random.randint(0, 255), "None")
slash = move("Slash", SRP, 1, random.randint(0, 255), "None")



#player is a placeholder for a chooseable name
#I am going to KILL MYSELF

player = me("Player", 10, 5, 5, 5, 0, 100, 782)
player.add_status("slorbed")
player.add_status("moist")
player.me_moveset(incin, shit_pants, meow, slash)

enemy1 = evil("Slorp", 10, 5, 5, 5, 90, 29, FIR)
enemy1.add_status("silly")

class battle:
    def __init__(self, player, enc_mob1, enc_mob2, enc_mob3):
        self.player = player
        self.enc_mob1 = enc_mob1
        self.enc_mob2 = enc_mob2
        self.enc_mob3 = enc_mob3
        pass
