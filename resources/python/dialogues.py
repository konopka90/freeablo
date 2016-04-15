# This script is responsible for managing dialogues
# depending on game progress

import freeablo
import docmanage
from random import randint

# Globals

ENTRY_SELECTED = '<span class="pentagon_left"/>%s<span class="pentagon_right"/>'
ENTRY_NOT_SELECTED = '<span style="visibility: hidden;" class="pentagon_left"/>%s<span style="visibility: hidden;" class="pentagon_right"/>'
DIALOGUE_PATH = "resources/gui/dialogues/"

onTradeFinishOpenDialogue = ""

def closeOtherWindows():
    docmanage.manager.hideDoc(docmanage.manager.PauseFile)
    docmanage.manager.hideDoc(docmanage.manager.InventoryFile)
    docmanage.manager.hideDoc(docmanage.manager.CharacterFile)
    docmanage.manager.hideDoc(docmanage.manager.SpellsFile)
    docmanage.manager.hideDoc(docmanage.manager.QuestFile)

def openDialogue(rml, openingSound):

    global DIALOGUE_PATH

    if openingSound != "":
        freeablo.playSound(openingSound)

    if rml != "":
        rml = DIALOGUE_PATH + rml
        freeablo.openDialogue(rml)


def openScrollbox(rml, openingSound, onFinishOpenDialogue = None):

    global DIALOGUE_PATH

    if openingSound != "":
        freeablo.playSound(openingSound)

    if rml != "":
        rml = DIALOGUE_PATH + rml
        if onFinishOpenDialogue is None:
            onFinishOpenDialogue = ""
        else:
            onFinishOpenDialogue = DIALOGUE_PATH + onFinishOpenDialogue

        freeablo.openDialogueScrollbox(rml, onFinishOpenDialogue)

def openTrade(rml):
    
    global onTradeFinishOpenDialogue

    openDialogue(rml, "")
    onTradeFinishOpenDialogue = "NPCsmith.rml"

def closeTrade():

    global onTradeFinishOpenDialogue

    freeablo.closeDialogue()
    openDialogue(onTradeFinishOpenDialogue, "")

def talkTo(npcId):

    print npcId

    closeOtherWindows()
    freeablo.stopSound()

    if npcId == 'NPCsmith':
        openDialogue("NPCsmith.rml","sfx/Towners/Bsmith44.wav")
    elif npcId == 'NPCstorytell':
        openDialogue("NPCstorytell.rml","sfx/Towners/storyt25.wav")
    elif npcId == 'NPCdrunk':
        openDialogue("NPCdrunk.rml","sfx/Towners/Drunk27.wav")
    elif npcId == 'NPChealer':
        openDialogue("NPChealer.rml","sfx/Towners/Healer37.wav")
    elif npcId == 'NPCboy':
        openDialogue("NPCboy.rml","sfx/Towners/Pegboy32.wav")
    elif npcId == 'NPCmaid':
        openDialogue("NPCmaid.rml","sfx/Towners/Bmaid31.wav")
    elif npcId == 'NPCwitch':
        openDialogue("NPCwitch.rml","sfx/Towners/Witch38.wav")
    elif npcId == 'NPCtavern':
        openScrollbox("NPCtavern.rml", "sfx/Towners/Tavown00.wav")
    elif npcId.startswith('NPCcow'):
        number = randint(1,2)
        openDialogue("", "sfx/Towners/Cow" + str(number) + ".wav")
