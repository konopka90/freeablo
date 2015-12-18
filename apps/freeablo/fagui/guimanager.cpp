#include "guimanager.h"

#include <Rocket/Core.h>

#include <input/hotkey.h>

#include "../farender/renderer.h"
#include "animateddecoratorinstancer.h"


namespace FAGui
{   
    Rocket::Core::ElementDocument* ingameUi = NULL;
    Rocket::Core::ElementDocument* mainMenu = NULL;
    Rocket::Core::ElementDocument* chooseClassMenu = NULL;
    Rocket::Core::ElementDocument* enterNameMenu = NULL;

    std::string GuiManager::invClass;

    GuiManager::GuiManager(FAWorld::Inventory & playerInventory, Engine::EngineMain& engine, std::string invClass) : mPythonFuncs(playerInventory, *this, engine)
    {

        this->invClass = invClass;
        initPython(mPythonFuncs);

        Input::Hotkey::initpythonwrapper();

        FARender::Renderer* renderer = FARender::Renderer::get();

        Rocket::Core::DecoratorInstancer* animInstancer = Rocket::Core::Factory::RegisterDecoratorInstancer("faanim", (Rocket::Core::DecoratorInstancer*)new AnimatedDecoratorInstancer(renderer->getRocketContext()->GetRenderInterface()));
        animInstancer->RemoveReference();

        ingameUi = renderer->getRocketContext()->LoadDocument("resources/gui/base.rml");
        mainMenu = renderer->getRocketContext()->LoadDocument("resources/gui/mainmenu.rml");
        chooseClassMenu = renderer->getRocketContext()->LoadDocument("resources/gui/creator_choose_class_menu.rml");
        enterNameMenu = renderer->getRocketContext()->LoadDocument("resources/gui/creator_enter_name_menu.rml");
    }

    void GuiManager::showIngameGui()
    {
        enterNameMenu->Hide();
        chooseClassMenu->Hide();
        mainMenu->Hide();
        ingameUi->Show();
        ingameUi->PushToBack(); // base.rml is an empty sheet that covers the whole screen for
        // detecting clicks outside the gui, push it to back so it doesn't
        // block clicks on the real gui.
    }


    void GuiManager::showMainMenu()
    {
        ingameUi->Hide();
        mainMenu->Show();
    }

    void GuiManager::showChooseClassMenu()
    {
        enterNameMenu->Hide();
        mainMenu->Hide();
        chooseClassMenu->Show();
    }

    void GuiManager::showEnterNameMenu(int classNumber)
    {
        chooseClassMenu->Hide();
        enterNameMenu->SetAttribute<int>("selectedClass", classNumber);
        enterNameMenu->Show();
    }

    void GuiManager::updateGui()
    {
        FARender::Renderer* renderer = FARender::Renderer::get();

        renderer->getRocketContext()->Update();
    }
}
