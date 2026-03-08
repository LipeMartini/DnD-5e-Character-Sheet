"""
Módulo para exportação de fichas de personagem em PDF
Requer: pip install reportlab
"""
from typing import Optional

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class CharacterPDFExporter:
    """Classe para exportar fichas de personagem em PDF"""
    
    @staticmethod
    def is_available() -> bool:
        """Verifica se a biblioteca reportlab está disponível"""
        return REPORTLAB_AVAILABLE
    
    @staticmethod
    def export_to_pdf(character, filepath: str) -> bool:
        """
        Exporta personagem para PDF formatado
        
        Args:
            character: Objeto Character
            filepath: Caminho do arquivo de destino
            
        Returns:
            True se sucesso, False caso contrário
        """
        if not REPORTLAB_AVAILABLE:
            raise Exception("A biblioteca 'reportlab' não está instalada. Execute: pip install reportlab")
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Estilos customizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#654321'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#8B4513'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Título
            story.append(Paragraph(f"<b>{character.name or 'Personagem sem nome'}</b>", title_style))
            
            # Informações básicas
            basic_info = [
                ['Raça:', character.race.name if character.race else 'N/A'],
                ['Subraça:', character.subrace.name if character.subrace else 'N/A'],
                ['Classe:', character.character_class.name if character.character_class else 'N/A'],
                ['Subclasse:', character.subclass_name or 'N/A'],
                ['Nível:', str(character.level)],
                ['Background:', character.background.name if character.background else 'N/A'],
                ['Alinhamento:', character.alignment or 'N/A'],
                ['XP:', str(character.experience_points)]
            ]
            
            basic_table = Table(basic_info, colWidths=[2*inch, 4*inch])
            basic_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5EBDC')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#654321')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B4513')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(basic_table)
            story.append(Spacer(1, 20))
            
            # Atributos
            story.append(Paragraph("<b>Atributos</b>", heading_style))
            
            stats_data = [
                ['Atributo', 'Valor', 'Modificador'],
                ['Força', str(character.stats.strength), f"{character.stats.get_modifier('strength'):+d}"],
                ['Destreza', str(character.stats.dexterity), f"{character.stats.get_modifier('dexterity'):+d}"],
                ['Constituição', str(character.stats.constitution), f"{character.stats.get_modifier('constitution'):+d}"],
                ['Inteligência', str(character.stats.intelligence), f"{character.stats.get_modifier('intelligence'):+d}"],
                ['Sabedoria', str(character.stats.wisdom), f"{character.stats.get_modifier('wisdom'):+d}"],
                ['Carisma', str(character.stats.charisma), f"{character.stats.get_modifier('charisma'):+d}"],
            ]
            
            stats_table = Table(stats_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4513')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFF8DC')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B4513')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # Combate
            story.append(Paragraph("<b>Combate</b>", heading_style))
            
            combat_data = [
                ['HP Máximo', 'HP Atual', 'HP Temporário', 'CA', 'Iniciativa', 'Velocidade', 'Bônus Prof.'],
                [
                    str(character.max_hit_points),
                    str(character.current_hit_points),
                    str(character.temporary_hit_points),
                    str(character.armor_class),
                    f"{character.initiative:+d}",
                    f"{character.speed} pés",
                    f"+{character.proficiency_bonus}"
                ]
            ]
            
            combat_table = Table(combat_data, colWidths=[1*inch] * 7)
            combat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4513')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFF8DC')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B4513')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(combat_table)
            story.append(Spacer(1, 20))
            
            # Proficiências em perícias
            if character.skill_proficiencies:
                story.append(Paragraph("<b>Proficiências em Perícias</b>", heading_style))
                skills_text = ", ".join(character.skill_proficiencies)
                story.append(Paragraph(skills_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Expertise
            if character.skill_expertise:
                story.append(Paragraph("<b>Expertise</b>", heading_style))
                expertise_text = ", ".join(character.skill_expertise)
                story.append(Paragraph(expertise_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Testes de resistência
            if character.saving_throw_proficiencies:
                story.append(Paragraph("<b>Testes de Resistência</b>", heading_style))
                saves_text = ", ".join(character.saving_throw_proficiencies)
                story.append(Paragraph(saves_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Idiomas
            if character.languages:
                story.append(Paragraph("<b>Idiomas</b>", heading_style))
                lang_text = ", ".join(character.languages)
                story.append(Paragraph(lang_text, styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Traits raciais
            if character.traits:
                story.append(Paragraph("<b>Traits Raciais</b>", heading_style))
                for trait in character.traits:
                    story.append(Paragraph(f"• {trait}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Class Features
            if character.class_features:
                story.append(Paragraph("<b>Class Features</b>", heading_style))
                for feature in character.class_features:
                    story.append(Paragraph(f"• {feature}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Feats
            if character.feats:
                story.append(Paragraph("<b>Feats</b>", heading_style))
                for feat in character.feats:
                    story.append(Paragraph(f"• {feat}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Fighting Styles
            if character.fighting_styles:
                story.append(Paragraph("<b>Fighting Styles</b>", heading_style))
                for style in character.fighting_styles:
                    story.append(Paragraph(f"• {style}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Spellcasting
            if character.spellcasting:
                story.append(PageBreak())
                story.append(Paragraph("<b>Conjuração</b>", heading_style))
                
                spell_info = [
                    ['Habilidade:', character.spellcasting.spellcasting_ability.capitalize()],
                    ['CD de Magia:', str(character.spellcasting.spell_save_dc)],
                    ['Bônus de Ataque:', f"+{character.spellcasting.spell_attack_bonus}"]
                ]
                
                spell_info_table = Table(spell_info, colWidths=[2*inch, 2*inch])
                spell_info_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5EBDC')),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B4513')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(spell_info_table)
                story.append(Spacer(1, 12))
                
                # Cantrips
                if character.spellcasting.known_cantrips:
                    story.append(Paragraph("<b>Cantrips Conhecidos</b>", heading_style))
                    for cantrip in character.spellcasting.known_cantrips:
                        story.append(Paragraph(f"• {cantrip}", styles['Normal']))
                    story.append(Spacer(1, 12))
                
                # Magias conhecidas
                if character.spellcasting.known_spells:
                    story.append(Paragraph("<b>Magias Conhecidas</b>", heading_style))
                    for spell in character.spellcasting.known_spells:
                        story.append(Paragraph(f"• {spell}", styles['Normal']))
                    story.append(Spacer(1, 12))
                
                # Magias preparadas
                if character.spellcasting.prepared_spells:
                    story.append(Paragraph("<b>Magias Preparadas</b>", heading_style))
                    for spell in character.spellcasting.prepared_spells:
                        story.append(Paragraph(f"• {spell}", styles['Normal']))
                    story.append(Spacer(1, 12))
            
            # Inventário
            if character.inventory:
                story.append(PageBreak())
                story.append(Paragraph("<b>Inventário</b>", heading_style))
                
                # Moedas
                currency_data = [
                    ['Cobre', 'Prata', 'Electrum', 'Ouro', 'Platina'],
                    [
                        str(character.inventory.copper),
                        str(character.inventory.silver),
                        str(character.inventory.electrum),
                        str(character.inventory.gold),
                        str(character.inventory.platinum)
                    ]
                ]
                
                currency_table = Table(currency_data, colWidths=[1.2*inch] * 5)
                currency_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B4513')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFF8DC')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B4513')),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(currency_table)
                story.append(Spacer(1, 12))
                
                # Armas
                if character.inventory.weapons:
                    story.append(Paragraph("<b>Armas</b>", heading_style))
                    for weapon in character.inventory.weapons:
                        equipped = " (Equipada)" if weapon.equipped else ""
                        story.append(Paragraph(f"• {weapon.name}{equipped}", styles['Normal']))
                    story.append(Spacer(1, 12))
                
                # Armaduras
                if character.inventory.armors:
                    story.append(Paragraph("<b>Armaduras</b>", heading_style))
                    for armor in character.inventory.armors:
                        equipped = " (Equipada)" if armor.equipped else ""
                        story.append(Paragraph(f"• {armor.name}{equipped}", styles['Normal']))
                    story.append(Spacer(1, 12))
                
                # Itens
                if character.inventory.items:
                    story.append(Paragraph("<b>Itens</b>", heading_style))
                    for item in character.inventory.items:
                        story.append(Paragraph(f"• {item.name} (x{item.quantity})", styles['Normal']))
                    story.append(Spacer(1, 12))
            
            # Notas
            if character.notes:
                story.append(PageBreak())
                story.append(Paragraph("<b>Notas</b>", heading_style))
                for category, content in character.notes.items():
                    story.append(Paragraph(f"<b>{category}:</b>", styles['Heading3']))
                    story.append(Paragraph(content, styles['Normal']))
                    story.append(Spacer(1, 12))
            
            # Gera o PDF
            doc.build(story)
            return True
            
        except Exception as e:
            raise Exception(f"Erro ao exportar para PDF: {str(e)}")
