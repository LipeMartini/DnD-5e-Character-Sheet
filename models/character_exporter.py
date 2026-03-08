"""
Módulo para exportação de fichas de personagem em múltiplos formatos
"""
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Optional
from pathlib import Path


class CharacterExporter:
    """Classe para exportar fichas de personagem em diferentes formatos"""
    
    @staticmethod
    def export_to_json(character, filepath: str) -> bool:
        """
        Exporta personagem para JSON
        
        Args:
            character: Objeto Character
            filepath: Caminho do arquivo de destino
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(character.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise Exception(f"Erro ao exportar para JSON: {str(e)}")
    
    @staticmethod
    def export_to_xml(character, filepath: str) -> bool:
        """
        Exporta personagem para XML
        
        Args:
            character: Objeto Character
            filepath: Caminho do arquivo de destino
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            root = ET.Element("character")
            
            # Informações básicas
            basic_info = ET.SubElement(root, "basic_info")
            ET.SubElement(basic_info, "name").text = character.name or ""
            ET.SubElement(basic_info, "level").text = str(character.level)
            ET.SubElement(basic_info, "alignment").text = character.alignment or ""
            ET.SubElement(basic_info, "experience_points").text = str(character.experience_points)
            
            # Raça
            if character.race:
                race_elem = ET.SubElement(root, "race")
                ET.SubElement(race_elem, "name").text = character.race.name
                ET.SubElement(race_elem, "size").text = character.race.size
                ET.SubElement(race_elem, "speed").text = str(character.race.speed)
                
                ability_bonuses = ET.SubElement(race_elem, "ability_bonuses")
                for stat, bonus in character.race.ability_bonuses.items():
                    bonus_elem = ET.SubElement(ability_bonuses, "bonus")
                    bonus_elem.set("stat", stat)
                    bonus_elem.text = str(bonus)
            
            # Subraça
            if character.subrace:
                subrace_elem = ET.SubElement(root, "subrace")
                ET.SubElement(subrace_elem, "name").text = character.subrace.name
                ET.SubElement(subrace_elem, "parent_race").text = character.subrace.parent_race
            
            # Classe
            if character.character_class:
                class_elem = ET.SubElement(root, "character_class")
                ET.SubElement(class_elem, "name").text = character.character_class.name
                ET.SubElement(class_elem, "hit_die").text = str(character.character_class.hit_die)
            
            # Subclasse
            if character.subclass_name:
                ET.SubElement(root, "subclass").text = character.subclass_name
            
            # Background
            if character.background:
                bg_elem = ET.SubElement(root, "background")
                ET.SubElement(bg_elem, "name").text = character.background.name
            
            # Atributos
            stats_elem = ET.SubElement(root, "stats")
            for stat_name in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
                stat_value = getattr(character.stats, stat_name, 10)
                ET.SubElement(stats_elem, stat_name).text = str(stat_value)
            
            base_stats_elem = ET.SubElement(root, "base_stats")
            for stat_name in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
                stat_value = getattr(character.base_stats, stat_name, 10)
                ET.SubElement(base_stats_elem, stat_name).text = str(stat_value)
            
            # Combate
            combat_elem = ET.SubElement(root, "combat")
            ET.SubElement(combat_elem, "max_hit_points").text = str(character.max_hit_points)
            ET.SubElement(combat_elem, "current_hit_points").text = str(character.current_hit_points)
            ET.SubElement(combat_elem, "temporary_hit_points").text = str(character.temporary_hit_points)
            ET.SubElement(combat_elem, "armor_class").text = str(character.armor_class)
            ET.SubElement(combat_elem, "initiative").text = str(character.initiative)
            ET.SubElement(combat_elem, "speed").text = str(character.speed)
            ET.SubElement(combat_elem, "proficiency_bonus").text = str(character.proficiency_bonus)
            
            # Proficiências
            proficiencies_elem = ET.SubElement(root, "proficiencies")
            
            skills_elem = ET.SubElement(proficiencies_elem, "skills")
            for skill in character.skill_proficiencies:
                ET.SubElement(skills_elem, "skill").text = skill
            
            expertise_elem = ET.SubElement(proficiencies_elem, "expertise")
            for skill in character.skill_expertise:
                ET.SubElement(expertise_elem, "skill").text = skill
            
            saves_elem = ET.SubElement(proficiencies_elem, "saving_throws")
            for save in character.saving_throw_proficiencies:
                ET.SubElement(saves_elem, "save").text = save
            
            weapons_elem = ET.SubElement(proficiencies_elem, "weapons")
            for weapon in character.weapon_proficiencies:
                ET.SubElement(weapons_elem, "weapon").text = weapon
            
            armors_elem = ET.SubElement(proficiencies_elem, "armors")
            for armor in character.armor_proficiencies:
                ET.SubElement(armors_elem, "armor").text = armor
            
            # Idiomas
            languages_elem = ET.SubElement(root, "languages")
            for lang in character.languages:
                ET.SubElement(languages_elem, "language").text = lang
            
            # Traits
            traits_elem = ET.SubElement(root, "traits")
            for trait in character.traits:
                ET.SubElement(traits_elem, "trait").text = trait
            
            # Class Features
            features_elem = ET.SubElement(root, "class_features")
            for feature in character.class_features:
                ET.SubElement(features_elem, "feature").text = feature
            
            # Feats
            feats_elem = ET.SubElement(root, "feats")
            for feat in character.feats:
                ET.SubElement(feats_elem, "feat").text = feat
            
            # Fighting Styles
            if character.fighting_styles:
                styles_elem = ET.SubElement(root, "fighting_styles")
                for style in character.fighting_styles:
                    ET.SubElement(styles_elem, "style").text = style
            
            # Spellcasting
            if character.spellcasting:
                spell_elem = ET.SubElement(root, "spellcasting")
                ET.SubElement(spell_elem, "ability").text = character.spellcasting.spellcasting_ability
                ET.SubElement(spell_elem, "spell_save_dc").text = str(character.spellcasting.spell_save_dc)
                ET.SubElement(spell_elem, "spell_attack_bonus").text = str(character.spellcasting.spell_attack_bonus)
                
                cantrips_elem = ET.SubElement(spell_elem, "known_cantrips")
                for cantrip in character.spellcasting.known_cantrips:
                    ET.SubElement(cantrips_elem, "cantrip").text = cantrip
                
                known_elem = ET.SubElement(spell_elem, "known_spells")
                for spell in character.spellcasting.known_spells:
                    ET.SubElement(known_elem, "spell").text = spell
                
                prepared_elem = ET.SubElement(spell_elem, "prepared_spells")
                for spell in character.spellcasting.prepared_spells:
                    ET.SubElement(prepared_elem, "spell").text = spell
            
            # Inventário
            if character.inventory:
                inv_elem = ET.SubElement(root, "inventory")
                
                # Moedas
                currency_elem = ET.SubElement(inv_elem, "currency")
                ET.SubElement(currency_elem, "copper").text = str(character.inventory.copper)
                ET.SubElement(currency_elem, "silver").text = str(character.inventory.silver)
                ET.SubElement(currency_elem, "electrum").text = str(character.inventory.electrum)
                ET.SubElement(currency_elem, "gold").text = str(character.inventory.gold)
                ET.SubElement(currency_elem, "platinum").text = str(character.inventory.platinum)
                
                # Armas
                weapons_inv = ET.SubElement(inv_elem, "weapons")
                for weapon in character.inventory.weapons:
                    weapon_elem = ET.SubElement(weapons_inv, "weapon")
                    ET.SubElement(weapon_elem, "name").text = weapon.name
                    ET.SubElement(weapon_elem, "equipped").text = str(weapon.equipped)
                
                # Armaduras
                armors_inv = ET.SubElement(inv_elem, "armors")
                for armor in character.inventory.armors:
                    armor_elem = ET.SubElement(armors_inv, "armor")
                    ET.SubElement(armor_elem, "name").text = armor.name
                    ET.SubElement(armor_elem, "equipped").text = str(armor.equipped)
                
                # Itens
                items_inv = ET.SubElement(inv_elem, "items")
                for item in character.inventory.items:
                    item_elem = ET.SubElement(items_inv, "item")
                    ET.SubElement(item_elem, "name").text = item.name
                    ET.SubElement(item_elem, "quantity").text = str(item.quantity)
            
            # Notas
            if character.notes:
                notes_elem = ET.SubElement(root, "notes")
                for category, content in character.notes.items():
                    note_elem = ET.SubElement(notes_elem, "note")
                    note_elem.set("category", category)
                    note_elem.text = content
            
            # Formata XML com indentação
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            
            return True
        except Exception as e:
            raise Exception(f"Erro ao exportar para XML: {str(e)}")
    
    @staticmethod
    def import_from_json(filepath: str):
        """
        Importa personagem de JSON
        
        Args:
            filepath: Caminho do arquivo JSON
            
        Returns:
            Objeto Character
        """
        try:
            from models import Character
            return Character.load_from_file(filepath)
        except Exception as e:
            raise Exception(f"Erro ao importar de JSON: {str(e)}")
    
    @staticmethod
    def import_from_xml(filepath: str):
        """
        Importa personagem de XML
        
        Args:
            filepath: Caminho do arquivo XML
            
        Returns:
            Objeto Character
        """
        try:
            from models import Character, Stats
            from models.race import RaceDatabase
            from models.subrace import SubraceDatabase
            from models.character_class import ClassDatabase
            from models.background import BackgroundDatabase
            from models import Inventory, Weapon, Armor, Item
            from models.spellcasting import SpellcastingInfo
            
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            character = Character()
            
            # Informações básicas
            basic = root.find('basic_info')
            if basic is not None:
                character.name = basic.findtext('name', '')
                character.level = int(basic.findtext('level', '1'))
                character.alignment = basic.findtext('alignment', 'Neutral')
                character.experience_points = int(basic.findtext('experience_points', '0'))
            
            # Atributos base
            base_stats_elem = root.find('base_stats')
            if base_stats_elem is not None:
                character.base_stats = Stats(
                    strength=int(base_stats_elem.findtext('strength', '10')),
                    dexterity=int(base_stats_elem.findtext('dexterity', '10')),
                    constitution=int(base_stats_elem.findtext('constitution', '10')),
                    intelligence=int(base_stats_elem.findtext('intelligence', '10')),
                    wisdom=int(base_stats_elem.findtext('wisdom', '10')),
                    charisma=int(base_stats_elem.findtext('charisma', '10'))
                )
            
            # Atributos atuais
            stats_elem = root.find('stats')
            if stats_elem is not None:
                character.stats = Stats(
                    strength=int(stats_elem.findtext('strength', '10')),
                    dexterity=int(stats_elem.findtext('dexterity', '10')),
                    constitution=int(stats_elem.findtext('constitution', '10')),
                    intelligence=int(stats_elem.findtext('intelligence', '10')),
                    wisdom=int(stats_elem.findtext('wisdom', '10')),
                    charisma=int(stats_elem.findtext('charisma', '10'))
                )
            
            # Combate
            combat = root.find('combat')
            if combat is not None:
                character.max_hit_points = int(combat.findtext('max_hit_points', '0'))
                character.current_hit_points = int(combat.findtext('current_hit_points', '0'))
                character.temporary_hit_points = int(combat.findtext('temporary_hit_points', '0'))
                character.armor_class = int(combat.findtext('armor_class', '10'))
                character.initiative = int(combat.findtext('initiative', '0'))
                character.speed = int(combat.findtext('speed', '30'))
                character.proficiency_bonus = int(combat.findtext('proficiency_bonus', '2'))
            
            # Proficiências
            prof = root.find('proficiencies')
            if prof is not None:
                skills = prof.find('skills')
                if skills is not None:
                    character.skill_proficiencies = [s.text for s in skills.findall('skill') if s.text]
                
                expertise = prof.find('expertise')
                if expertise is not None:
                    character.skill_expertise = [s.text for s in expertise.findall('skill') if s.text]
                
                saves = prof.find('saving_throws')
                if saves is not None:
                    character.saving_throw_proficiencies = [s.text for s in saves.findall('save') if s.text]
                
                weapons = prof.find('weapons')
                if weapons is not None:
                    character.weapon_proficiencies = [w.text for w in weapons.findall('weapon') if w.text]
                
                armors = prof.find('armors')
                if armors is not None:
                    character.armor_proficiencies = [a.text for a in armors.findall('armor') if a.text]
            
            # Idiomas
            languages = root.find('languages')
            if languages is not None:
                character.languages = [l.text for l in languages.findall('language') if l.text]
            
            # Traits
            traits = root.find('traits')
            if traits is not None:
                character.traits = [t.text for t in traits.findall('trait') if t.text]
            
            # Class Features
            features = root.find('class_features')
            if features is not None:
                character.class_features = [f.text for f in features.findall('feature') if f.text]
            
            # Feats
            feats = root.find('feats')
            if feats is not None:
                character.feats = [f.text for f in feats.findall('feat') if f.text]
            
            # Fighting Styles
            styles = root.find('fighting_styles')
            if styles is not None:
                character.fighting_styles = [s.text for s in styles.findall('style') if s.text]
            
            # Raça
            race_elem = root.find('race')
            if race_elem is not None:
                race_name = race_elem.findtext('name')
                if race_name:
                    all_races = RaceDatabase.get_all_races()
                    if race_name in all_races:
                        character.race = all_races[race_name]
            
            # Subraça
            subrace_elem = root.find('subrace')
            if subrace_elem is not None:
                subrace_name = subrace_elem.findtext('name')
                if subrace_name:
                    all_subraces = SubraceDatabase.get_all_subraces()
                    if subrace_name in all_subraces:
                        character.subrace = all_subraces[subrace_name]
            
            # Classe
            class_elem = root.find('character_class')
            if class_elem is not None:
                class_name = class_elem.findtext('name')
                if class_name:
                    all_classes = ClassDatabase.get_all_classes()
                    if class_name in all_classes:
                        character.character_class = all_classes[class_name]
            
            # Background
            bg_elem = root.find('background')
            if bg_elem is not None:
                bg_name = bg_elem.findtext('name')
                if bg_name:
                    all_backgrounds = BackgroundDatabase.get_all_backgrounds()
                    if bg_name in all_backgrounds:
                        character.background = all_backgrounds[bg_name]
            
            # Subclasse
            subclass = root.find('subclass')
            if subclass is not None and subclass.text:
                character.subclass_name = subclass.text
            
            # Spellcasting
            spell_elem = root.find('spellcasting')
            if spell_elem is not None:
                character.spellcasting = SpellcastingInfo()
                character.spellcasting.spellcasting_ability = spell_elem.findtext('ability', 'intelligence')
                character.spellcasting.spell_save_dc = int(spell_elem.findtext('spell_save_dc', '8'))
                character.spellcasting.spell_attack_bonus = int(spell_elem.findtext('spell_attack_bonus', '0'))
                
                cantrips = spell_elem.find('known_cantrips')
                if cantrips is not None:
                    character.spellcasting.known_cantrips = [c.text for c in cantrips.findall('cantrip') if c.text]
                
                known = spell_elem.find('known_spells')
                if known is not None:
                    character.spellcasting.known_spells = [s.text for s in known.findall('spell') if s.text]
                
                prepared = spell_elem.find('prepared_spells')
                if prepared is not None:
                    character.spellcasting.prepared_spells = [s.text for s in prepared.findall('spell') if s.text]
            
            # Inventário
            inv_elem = root.find('inventory')
            if inv_elem is not None:
                character.inventory = Inventory()
                
                currency = inv_elem.find('currency')
                if currency is not None:
                    character.inventory.copper = int(currency.findtext('copper', '0'))
                    character.inventory.silver = int(currency.findtext('silver', '0'))
                    character.inventory.electrum = int(currency.findtext('electrum', '0'))
                    character.inventory.gold = int(currency.findtext('gold', '0'))
                    character.inventory.platinum = int(currency.findtext('platinum', '0'))
            
            # Notas
            notes_elem = root.find('notes')
            if notes_elem is not None:
                character.notes = {}
                for note in notes_elem.findall('note'):
                    category = note.get('category', 'General')
                    content = note.text or ''
                    character.notes[category] = content
            
            return character
            
        except Exception as e:
            raise Exception(f"Erro ao importar de XML: {str(e)}")
