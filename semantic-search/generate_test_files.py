#!/usr/bin/env python3
"""
生成Unreal Engine风格的游戏资产测试文件
用于测试语义搜索功能
"""

import os
from pathlib import Path

def create_test_assets():
    """创建测试游戏资产文件夹结构和文件"""
    
    # 基础目录
    base_dir = Path("TestGameAssets_MysticRealms")
    
    # 游戏资产分类和文件定义
    assets = {
        "Textures": {
            "Characters": [
                "T_Warrior_Diffuse.tga", "T_Warrior_Normal.tga", "T_Warrior_Roughness.tga",
                "T_Mage_Diffuse.tga", "T_Mage_Normal.tga", "T_Mage_Emissive.tga",
                "T_Rogue_Diffuse.tga", "T_Rogue_Normal.tga", "T_Rogue_Metallic.tga",
                "T_Dragon_Scales_Diffuse.tga", "T_Dragon_Scales_Normal.tga",
                "T_Goblin_Skin_Diffuse.tga", "T_Goblin_Skin_Normal.tga",
                "T_Elf_Face_Diffuse.tga", "T_Elf_Ears_Normal.tga",
                "T_Dwarf_Beard_Diffuse.tga", "T_Dwarf_Armor_Metallic.tga",
                "T_Orc_Warpaint_Diffuse.tga", "T_Orc_Tusks_Normal.tga"
            ],
            "Environment": [
                "T_Stone_Wall_Diffuse.tga", "T_Stone_Wall_Normal.tga", "T_Stone_Wall_Height.tga",
                "T_Grass_Ground_Diffuse.tga", "T_Grass_Ground_Normal.tga",
                "T_Wood_Plank_Diffuse.tga", "T_Wood_Plank_Normal.tga", "T_Wood_Plank_Roughness.tga",
                "T_Metal_Rust_Diffuse.tga", "T_Metal_Rust_Metallic.tga", "T_Metal_Rust_Normal.tga",
                "T_Crystal_Cave_Diffuse.tga", "T_Crystal_Cave_Emissive.tga",
                "T_Lava_Rock_Diffuse.tga", "T_Lava_Rock_Emissive.tga", "T_Lava_Rock_Normal.tga",
                "T_Ice_Surface_Diffuse.tga", "T_Ice_Surface_Normal.tga", "T_Ice_Surface_Opacity.tga",
                "T_Sand_Desert_Diffuse.tga", "T_Sand_Desert_Normal.tga", "T_Sand_Desert_Height.tga"
            ],
            "Items": [
                "T_Sword_Excalibur_Diffuse.tga", "T_Sword_Excalibur_Normal.tga", "T_Sword_Excalibur_Metallic.tga",
                "T_Shield_Dragon_Diffuse.tga", "T_Shield_Dragon_Normal.tga",
                "T_Potion_Health_Diffuse.tga", "T_Potion_Health_Emissive.tga",
                "T_Potion_Mana_Diffuse.tga", "T_Potion_Mana_Emissive.tga",
                "T_Gem_Ruby_Diffuse.tga", "T_Gem_Ruby_Emissive.tga",
                "T_Gem_Sapphire_Diffuse.tga", "T_Gem_Emerald_Diffuse.tga",
                "T_Coin_Gold_Diffuse.tga", "T_Coin_Gold_Metallic.tga",
                "T_Scroll_Magic_Diffuse.tga", "T_Scroll_Magic_Normal.tga"
            ]
        },
        
        "Materials": {
            "Characters": [
                "M_Warrior_Body.uasset", "M_Warrior_Hair.uasset", "M_Warrior_Eyes.uasset",
                "M_Mage_Robe.uasset", "M_Mage_Staff.uasset", "M_Mage_Aura.uasset",
                "M_Rogue_Leather.uasset", "M_Rogue_Cloak.uasset", "M_Rogue_Dagger.uasset",
                "M_Dragon_Scales.uasset", "M_Dragon_Fire.uasset", "M_Dragon_Wings.uasset",
                "M_Goblin_Skin.uasset", "M_Goblin_Cloth.uasset",
                "M_Elf_Skin.uasset", "M_Elf_Clothing.uasset",
                "M_Dwarf_Beard.uasset", "M_Dwarf_Chainmail.uasset",
                "M_Orc_Skin.uasset", "M_Orc_Warpaint.uasset"
            ],
            "Environment": [
                "M_Stone_Castle.uasset", "M_Stone_Dungeon.uasset", "M_Stone_Bridge.uasset",
                "M_Wood_Tavern.uasset", "M_Wood_Ship.uasset", "M_Wood_Tree.uasset",
                "M_Metal_Gate.uasset", "M_Metal_Armor.uasset", "M_Metal_Weapon.uasset",
                "M_Crystal_Magic.uasset", "M_Crystal_Cave.uasset", "M_Crystal_Tower.uasset",
                "M_Lava_Flow.uasset", "M_Lava_Pool.uasset", "M_Lava_Rock.uasset",
                "M_Ice_Glacier.uasset", "M_Ice_Spike.uasset", "M_Ice_Palace.uasset",
                "M_Sand_Dune.uasset", "M_Sand_Storm.uasset", "M_Sand_Pyramid.uasset"
            ],
            "Effects": [
                "M_Fire_Spell.uasset", "M_Ice_Spell.uasset", "M_Lightning_Spell.uasset",
                "M_Healing_Aura.uasset", "M_Shield_Barrier.uasset", "M_Teleport_Portal.uasset",
                "M_Poison_Cloud.uasset", "M_Blood_Splatter.uasset", "M_Magic_Circle.uasset",
                "M_Smoke_Effect.uasset", "M_Dust_Cloud.uasset", "M_Sparkle_Trail.uasset"
            ]
        },
        
        "Meshes": {
            "Characters": [
                "SM_Warrior_Body.uasset", "SK_Warrior_Animated.uasset",
                "SM_Mage_Staff.uasset", "SK_Mage_Robes.uasset",
                "SM_Rogue_Dagger.uasset", "SK_Rogue_Cloak.uasset",
                "SM_Dragon_Head.uasset", "SK_Dragon_Full.uasset", "SM_Dragon_Wing.uasset",
                "SM_Goblin_Club.uasset", "SK_Goblin_Body.uasset",
                "SM_Elf_Bow.uasset", "SK_Elf_Archer.uasset",
                "SM_Dwarf_Axe.uasset", "SK_Dwarf_Warrior.uasset",
                "SM_Orc_Hammer.uasset", "SK_Orc_Berserker.uasset"
            ],
            "Environment": [
                "SM_Castle_Wall.uasset", "SM_Castle_Tower.uasset", "SM_Castle_Gate.uasset",
                "SM_Tree_Oak.uasset", "SM_Tree_Pine.uasset", "SM_Tree_Dead.uasset",
                "SM_Rock_Boulder.uasset", "SM_Rock_Cliff.uasset", "SM_Rock_Cave.uasset",
                "SM_Bridge_Stone.uasset", "SM_Bridge_Wood.uasset", "SM_Bridge_Rope.uasset",
                "SM_Building_Tavern.uasset", "SM_Building_Shop.uasset", "SM_Building_Temple.uasset",
                "SM_Pillar_Marble.uasset", "SM_Pillar_Stone.uasset", "SM_Pillar_Crystal.uasset"
            ],
            "Props": [
                "SM_Chest_Treasure.uasset", "SM_Chest_Wooden.uasset", "SM_Chest_Magic.uasset",
                "SM_Barrel_Wood.uasset", "SM_Barrel_Metal.uasset", "SM_Barrel_Poison.uasset",
                "SM_Table_Tavern.uasset", "SM_Chair_Throne.uasset", "SM_Bed_Royal.uasset",
                "SM_Torch_Wall.uasset", "SM_Torch_Standing.uasset", "SM_Lantern_Magic.uasset",
                "SM_Cauldron_Witch.uasset", "SM_Crystal_Ball.uasset", "SM_Anvil_Blacksmith.uasset"
            ]
        },
        
        "Audio": {
            "Music": [
                "SFX_Music_MainTheme.wav", "SFX_Music_Battle.wav", "SFX_Music_Victory.wav",
                "SFX_Music_Tavern.wav", "SFX_Music_Forest.wav", "SFX_Music_Dungeon.wav",
                "SFX_Music_Boss.wav", "SFX_Music_Credits.wav", "SFX_Music_Sad.wav"
            ],
            "Effects": [
                "SFX_Sword_Clang.wav", "SFX_Sword_Slash.wav", "SFX_Sword_Draw.wav",
                "SFX_Magic_Fireball.wav", "SFX_Magic_Healing.wav", "SFX_Magic_Lightning.wav",
                "SFX_Dragon_Roar.wav", "SFX_Dragon_Fly.wav", "SFX_Dragon_Fire.wav",
                "SFX_Footstep_Stone.wav", "SFX_Footstep_Grass.wav", "SFX_Footstep_Water.wav",
                "SFX_Door_Open.wav", "SFX_Door_Close.wav", "SFX_Door_Creak.wav",
                "SFX_Coin_Drop.wav", "SFX_Coin_Collect.wav", "SFX_Potion_Drink.wav"
            ],
            "Ambient": [
                "SFX_Wind_Forest.wav", "SFX_Water_Stream.wav", "SFX_Fire_Crackling.wav",
                "SFX_Cave_Dripping.wav", "SFX_Thunder_Storm.wav", "SFX_Birds_Chirping.wav",
                "SFX_Wolves_Howling.wav", "SFX_Ocean_Waves.wav", "SFX_Rain_Heavy.wav"
            ]
        },
        
        "Animations": {
            "Characters": [
                "A_Warrior_Idle.uasset", "A_Warrior_Walk.uasset", "A_Warrior_Run.uasset",
                "A_Warrior_Attack.uasset", "A_Warrior_Block.uasset", "A_Warrior_Death.uasset",
                "A_Mage_Cast.uasset", "A_Mage_Channel.uasset", "A_Mage_Teleport.uasset",
                "A_Rogue_Stealth.uasset", "A_Rogue_Backstab.uasset", "A_Rogue_Dodge.uasset",
                "A_Dragon_Fly.uasset", "A_Dragon_Land.uasset", "A_Dragon_Breathe.uasset",
                "A_Goblin_Dance.uasset", "A_Elf_Shoot.uasset", "A_Dwarf_Swing.uasset"
            ],
            "Interactions": [
                "A_Door_Open.uasset", "A_Chest_Open.uasset", "A_Lever_Pull.uasset",
                "A_Button_Press.uasset", "A_Climb_Ladder.uasset", "A_Swim_Underwater.uasset"
            ]
        },
        
        "Blueprints": {
            "Characters": [
                "BP_PlayerWarrior.uasset", "BP_PlayerMage.uasset", "BP_PlayerRogue.uasset",
                "BP_EnemyGoblin.uasset", "BP_EnemyOrc.uasset", "BP_EnemyDragon.uasset",
                "BP_NPCMerchant.uasset", "BP_NPCGuard.uasset", "BP_NPCWizard.uasset"
            ],
            "Items": [
                "BP_Weapon_Sword.uasset", "BP_Weapon_Bow.uasset", "BP_Weapon_Staff.uasset",
                "BP_Armor_Leather.uasset", "BP_Armor_Chainmail.uasset", "BP_Armor_Plate.uasset",
                "BP_Potion_Health.uasset", "BP_Potion_Mana.uasset", "BP_Potion_Strength.uasset",
                "BP_Treasure_Chest.uasset", "BP_Magic_Crystal.uasset", "BP_Ancient_Scroll.uasset"
            ],
            "Environment": [
                "BP_Door_Castle.uasset", "BP_Door_Wooden.uasset", "BP_Door_Magic.uasset",
                "BP_Trap_Spike.uasset", "BP_Trap_Arrow.uasset", "BP_Trap_Magic.uasset",
                "BP_Platform_Moving.uasset", "BP_Bridge_Drawbridge.uasset", "BP_Teleporter.uasset"
            ]
        },
        
        "UI": {
            "HUD": [
                "WBP_MainHUD.uasset", "WBP_HealthBar.uasset", "WBP_ManaBar.uasset",
                "WBP_Minimap.uasset", "WBP_ChatBox.uasset", "WBP_Crosshair.uasset"
            ],
            "Menus": [
                "WBP_MainMenu.uasset", "WBP_PauseMenu.uasset", "WBP_SettingsMenu.uasset",
                "WBP_InventoryMenu.uasset", "WBP_ShopMenu.uasset", "WBP_CraftingMenu.uasset",
                "WBP_QuestLog.uasset", "WBP_CharacterSheet.uasset", "WBP_SkillTree.uasset"
            ],
            "Icons": [
                "UI_Icon_Sword.png", "UI_Icon_Shield.png", "UI_Icon_Bow.png",
                "UI_Icon_Staff.png", "UI_Icon_Potion.png", "UI_Icon_Coin.png",
                "UI_Icon_Gem.png", "UI_Icon_Key.png", "UI_Icon_Scroll.png",
                "UI_Icon_Heart.png", "UI_Icon_Mana.png", "UI_Icon_Experience.png"
            ]
        },
        
        "VFX": {
            "Magic": [
                "VFX_Fireball_Explosion.uasset", "VFX_Lightning_Strike.uasset", "VFX_Ice_Shard.uasset",
                "VFX_Healing_Light.uasset", "VFX_Teleport_Portal.uasset", "VFX_Magic_Aura.uasset",
                "VFX_Poison_Cloud.uasset", "VFX_Shield_Barrier.uasset", "VFX_Energy_Beam.uasset"
            ],
            "Combat": [
                "VFX_Blood_Splatter.uasset", "VFX_Sword_Trail.uasset", "VFX_Arrow_Trail.uasset",
                "VFX_Hit_Sparks.uasset", "VFX_Dodge_Blur.uasset", "VFX_Critical_Hit.uasset"
            ],
            "Environment": [
                "VFX_Torch_Flame.uasset", "VFX_Waterfall_Mist.uasset", "VFX_Dust_Particles.uasset",
                "VFX_Leaves_Falling.uasset", "VFX_Snow_Falling.uasset", "VFX_Rain_Drops.uasset"
            ]
        }
    }
    
    print(f"🎮 开始生成游戏资产测试文件...")
    print(f"📁 目标目录: {base_dir}")
    
    total_files = 0
    
    # 创建基础目录
    base_dir.mkdir(exist_ok=True)
    
    # 遍历所有分类和子分类
    for category, subcategories in assets.items():
        category_path = base_dir / category
        category_path.mkdir(exist_ok=True)
        
        for subcategory, files in subcategories.items():
            subcategory_path = category_path / subcategory
            subcategory_path.mkdir(exist_ok=True)
            
            # 创建文件
            for filename in files:
                file_path = subcategory_path / filename
                file_path.touch()  # 创建空文件
                total_files += 1
    
    # 创建一些额外的有趣文件
    extra_files = [
        "README_GameAssets.md",
        "AssetList_MysticRealms.xlsx", 
        "GameDesignDocument_v2.pdf",
        "ArtStyle_Reference.psd",
        "SoundDesign_Notes.txt",
        "Performance_Guidelines.docx"
    ]
    
    for filename in extra_files:
        file_path = base_dir / filename
        file_path.touch()
        total_files += 1
    
    print(f"✅ 完成！")
    print(f"📊 统计信息:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 主要分类: {len(assets)}")
    print(f"   - 目录结构: {base_dir}")
    print(f"")
    print(f"🔍 现在你可以用语义搜索测试以下内容:")
    print(f"   - '战士' -> 找到 Warrior 相关文件")
    print(f"   - '魔法' -> 找到 Magic, Mage, Spell 相关文件") 
    print(f"   - '音效' -> 找到 SFX, Audio 相关文件")
    print(f"   - '贴图' -> 找到 Texture, T_ 前缀文件")
    print(f"   - '龙' -> 找到 Dragon 相关资产")
    print(f"   - '武器' -> 找到 Weapon, Sword, Bow 等文件")
    print(f"   - '界面' -> 找到 UI, WBP_ 相关文件")

if __name__ == "__main__":
    create_test_assets() 