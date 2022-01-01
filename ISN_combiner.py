import copy
import glob
#   ToDo List
#   Setup loop with correct divisiors and additions to get _3x1_2x1 and _4x1_2x1    -   Complete         
#   Setup loop to get Flight Decks                                                  -   Complete
#   Setup Matrix Combiner                                                           -   Complete
#   Add Exception Combiations ie (2x4 and CHL_025/CHL_030) (4x2 CHL_025/CHL_030)    -   Complete
#   Setup Module Output of results to new file                                      -   Complete
#   Setup loop for Cruiser Guns                                                     -   Complete
#   Setup loop with correct divisiors to get x02 x03 3x1 4x1                        -   Complete
#   Create 2x1 for 13+ calabers                                                     -   Complete
#   Setup .gfx links for module icons                                               -   Complete
#       and category icons                                                          -   Complete                                               
#   Setup .gfx links for topviews (probably blanks)									-	Complete
#   Setup discount ic stuff    Normal Capital                                       -   Complete
#   Setup discount ic stuff    Mixed Capital                                        -   Complete
#   Setup discount ic stuff    PB Cruiser                                           -   Complete
#   Setup discount ic stuff    Cruiser                                              -   Complete
#   Create techs                                                                    -   Big Complete
#   Create events                                                                   -   Complete
#   Create Module Localisation                                                      -   Complete
#       National Gun Names                                                          -   Complete
#   Create Tech Localisation                                                        -   Complete
#   Setup loop with correct divisiors to get size 10 hangers                        -   Complete
#   Change Normal Cruiser gun catagories to incude caliber  L/H						-	Complete
#   Submarine Turrets
#        Modules                                                                    -   Complete
#        Events                                                                     -   Complete
#        Techs                                                                      -   Complete
#        Localisation                                                               -   Complete
#        module icons                                                               -   Complete
#        Add Sub visibility values                                                  -   May Need Balancing
#        4" Turrets                                                                 -   Complete
#        Treaty limits                                                              -
#   BICE Supprot                                                                    -   Need to run test case
#       Update for changes in tech names                                           	-   Discontinued
#   Top View																		-   Complete
#   1.11 hanger modules

BICE = True

class DefModule:
    name = ""
    category = ""
    gui_category = ""
    parent = ""
    add_equipment_type = ""
    caliber = 0.0       # for keeping guns similar when merging
    level = 0           # for keeping guns similar when merging
    numberGuns = 0
    numberTurrets = 0
    dualPurpse = False
    manpower = 0.0
    #add_stats
    add_build_cost_ic = 0.0
    add_max_strength = 0.0
    add_hg_attack = 0.0
    add_lg_attack = 0.0
    add_anti_air_attack = 0.0
    add_supply_consumption = 0.0
    add_surface_visibility = 0.0
    add_carrier_size = 0
    add_sub_visibility = 0.0
    add_fuel_consumption = 0.0
    #add_average_stats
    av_hg_armor_piercing = 0.0
    av_lg_armor_piercing = 0.0
    #multiply_stats
    mp_build_cost_ic = 0.0
    mp_reliability = 0.0
    mp_naval_speed = 0.0
    mp_fuel_consumption = 0.0
    mp_max_strength = 0.0
    mp_armor_value = 0.0
    #build_cost_resources
    res_steel = 0.0
    res_chromium = 0.0
    critical_parts = ""
    #dismantle_cost_ic
    dismantle_cost_ic = 0.0
    ic_one_turret = 0.0
    ic_one_turret_a = 0.0
    ic_one_gun = 0.0
    category2 = ""
    def __repr__(self):
        return self.name

class DefTechEvents:
    name = ""
    gunTech = ""
    gunTech2 = ""
    launcherTech = ""
    hangerTech = ""
    treatyCompliant = True

def Matrix_combiner(gun, deck, array):
    convDeck = 1
    if "CHL" in deck.name:
        convDeck = .8

    hybrid = copy.deepcopy(gun)
    hybrid.name = hybrid.name + deck.name[-8:]
    #hybrid.category = hybrid.category + deck.category[-8:-4] #just throw them in with the regular modules
    hybrid.category = hybrid.category + "_CV"    #Just merg the converted and armored together
    hybrid.gui_category = hybrid.gui_category
    if hybrid.parent != "":
        hybrid.parent += deck.name[-8:]
    #hybrid.gui_category = hybrid.gui_category + "_cv"   #merges all hanger types together into one sub menu
    #hybrid.gui_category = hybrid.gui_category + deck.gui_category[-4:]
    hybrid.manpower += deck.manpower
    hybrid.add_build_cost_ic += deck.add_build_cost_ic*convDeck
    hybrid.add_max_strength += deck.add_max_strength/2
    hybrid.add_supply_consumption += deck.add_supply_consumption
    hybrid.add_surface_visibility += deck.add_surface_visibility
    hybrid.add_carrier_size += deck.add_carrier_size
    hybrid.mp_build_cost_ic += deck.mp_build_cost_ic
    hybrid.mp_reliability += deck.mp_reliability
    hybrid.mp_naval_speed += deck.mp_naval_speed
    hybrid.mp_fuel_consumption += deck.mp_fuel_consumption
    hybrid.mp_max_strength += deck.mp_max_strength
    hybrid.add_fuel_consumption += deck.add_fuel_consumption

    if "capital" in hybrid.name and hybrid.add_carrier_size > 21: #Added for long flight deck sprites
        hybrid.category2 = hybrid.category + "_long"
    elif "capital" in hybrid.name and hybrid.add_carrier_size < 21:
        hybrid.category2 = hybrid.category
    if "cruiser" in hybrid.name and hybrid.add_carrier_size > 16:
        hybrid.category2 = hybrid.category + "_long"
    elif "cruiser" in hybrid.name and hybrid.add_carrier_size < 16:
        hybrid.category2 = hybrid.category

    #bunch of conditions for hanger size and armor reduction
    tmp_armor_mult = 1

    if deck.name.find("_AHL_") >-1:
        tmp_armor_mult = (tmp_armor_mult*.75)

    if deck.name.find("030") >-1 or (gun.name.find("cruiser") >-1 and deck.name.find("020") >-1):
        hybrid.mp_armor_value += deck.mp_armor_value*tmp_armor_mult
    elif deck.name.find("025") >-1 or (gun.name.find("cruiser") >-1 and deck.name.find("015") >-1):
        hybrid.mp_armor_value += deck.mp_armor_value*tmp_armor_mult*.75
    else:
        hybrid.mp_armor_value += deck.mp_armor_value*tmp_armor_mult*.5
    hybrid.dismantle_cost_ic += deck.dismantle_cost_ic

    array.append(hybrid)

def Module_outputer(module_array, file):
    moduleGroup = open(file, "w")
    tmpfile = file.split("\\")

    gfx_moduleGroup = open("Output\\interface\\%s_.gfx"%tmpfile[len(tmpfile)-1][:(tmpfile[len(tmpfile)-1].find("."))], "w")
    Sub_UnitModule = open("Output\\_module lists\\%s_Sub-Unit.txt"%tmpfile[len(tmpfile)-1][:(tmpfile[len(tmpfile)-1].find("."))], "w")  

    #print(gfx_moduleGroup.name)

    moduleGroup.write("equipment_modules = {\n")
    gfx_moduleGroup.write("spriteTypes = {\n")

    for module in module_array:
        moduleGroup.write("\n\t%s = {"%module.name)
        #moduleGroup.write("\n\t\tcategory = %s"%module.category)
        moduleGroup.write("\n\t\tcategory = %s"%module.category)    #maybe get better results from ai ship desings?
        #if module.caliber <5.9:
        #    moduleGroup.write("\n\t\tcategory = %sL_%s"%(module.gui_category[:-3],module.gui_category[-3:]))
        #elif module.caliber >5.9 and module.caliber <8.1:
        #    moduleGroup.write("\n\t\tcategory = %sH_%s"%(module.gui_category[:-3],module.gui_category[-3:]))
        #else:
        #    moduleGroup.write("\n\t\tcategory = %s"%module.gui_category)

        if ("capital" in module.name and module.add_carrier_size > 21) or ("cruiser" in module.name and module.add_carrier_size > 16): #new category for long flight decks
            moduleGroup.write("_long")

        moduleGroup.write("\n\t\tgui_category = %s"%module.gui_category)
        moduleGroup.write("\n\t\tsfx = sfx_ui_sd_module_turret")

        if module.parent != "":
            moduleGroup.write("\n\t\tparent = %s"%module.parent)
        if module.add_equipment_type != "":
            moduleGroup.write("\n\n\t\tadd_equipment_type = %s"%module.add_equipment_type)

        #allow module catagories
        allowModuleListShort = ["lic_hybrid_deck_hanger","nrm_carrier_airgroup_RC","nrm_carrier_airgroup_ASW"]
        allowModuleListLong = ["lic_hybrid_deck_hanger","nrm_carrier_airgroup_RC","nrm_carrier_airgroup_RC_L","nrm_carrier_airgroup_ASW","nrm_carrier_airgroup_ASW_L"]
        if module.add_carrier_size > 0:
            moduleGroup.write("\n\n\t\tallowed_module_categories = {")
            moduleGroup.write("\n\t\t\tcustom_slot_1 = {")
            moduleGroup.write("\n\t\t\t\tlic_hybrid_deck_style")
            moduleGroup.write("\n\t\t\t}")
            if ("capital" in module.name and module.add_carrier_size > 21) or ("cruiser" in module.name and module.add_carrier_size > 16):
                moduleGroup.write("\n\t\t\tcustom_slot_2 = {")
                for e in allowModuleListLong:
                    moduleGroup.write("\n\t\t\t\t%s"%e)
                moduleGroup.write("\n\t\t\t}")
                if ("capital" in module.name and module.add_carrier_size > 21):
                    moduleGroup.write("\n\t\t\tcustom_slot_3 = {")
                    for e in allowModuleListLong:
                        moduleGroup.write("\n\t\t\t\t%s"%e)
                    moduleGroup.write("\n\t\t\t}")
            else:
                moduleGroup.write("\n\t\t\tcustom_slot_2 = {")
                for e in allowModuleListShort:
                    moduleGroup.write("\n\t\t\t\t%s"%e)
                if (module.add_carrier_size>16):
                    moduleGroup.write("\n\t\t\t\t%nrm_carrier_airgroup_RC_L")
                    moduleGroup.write("\n\t\t\t\t%nrm_carrier_airgroup_AWS_L")
                moduleGroup.write("\n\t\t\t}")
            moduleGroup.write("\n\t\t}")

        moduleGroup.write("\n\n\t\tmanpower = %d"%module.manpower)
        #add_stats
        moduleGroup.write("\n\t\tadd_stats = {")
        moduleGroup.write("\n\t\t\tbuild_cost_ic = %s"%module.add_build_cost_ic)
        moduleGroup.write("\n\t\t\tmax_strength = %s"%module.add_max_strength)
        if module.add_hg_attack != 0:
            moduleGroup.write("\n\t\t\thg_attack = %s"%module.add_hg_attack)
        if module.add_lg_attack != 0:
            moduleGroup.write("\n\t\t\tlg_attack = %s"%module.add_lg_attack)
        if module.add_anti_air_attack != 0:
            moduleGroup.write("\n\t\t\tanti_air_attack = %s"%module.add_anti_air_attack)
        if module.add_fuel_consumption !=0:
            moduleGroup.write("\n\t\t\tfuel_consumption = %s"%module.add_fuel_consumption)
        moduleGroup.write("\n\t\t\tsupply_consumption = %s"%module.add_supply_consumption)
        moduleGroup.write("\n\t\t\tsurface_visibility = %s"%module.add_surface_visibility)
        moduleGroup.write("\n\t\t\tcarrier_size = %s"%module.add_carrier_size)
        moduleGroup.write("\n\t\t}")

        #add_average_stats
        moduleGroup.write("\n\t\tadd_average_stats = {")
        if module.av_hg_armor_piercing != 0:
            moduleGroup.write("\n\t\t\thg_armor_piercing = %s"%module.av_hg_armor_piercing)
        if module.av_lg_armor_piercing != 0:
            moduleGroup.write("\n\t\t\tlg_armor_piercing = %s"%module.av_lg_armor_piercing)
        moduleGroup.write("\n\t\t}")

        #multiply_stats
        moduleGroup.write("\n\t\tmultiply_stats = {")
        moduleGroup.write("\n\t\t\tbuild_cost_ic = %s"%module.mp_build_cost_ic)
        moduleGroup.write("\n\t\t\treliability = %s"%module.mp_reliability)
        moduleGroup.write("\n\t\t\tnaval_speed = %s"%module.mp_naval_speed)
        moduleGroup.write("\n\t\t\tfuel_consumption = %s"%module.mp_fuel_consumption)
        if module.mp_max_strength != 0:
            moduleGroup.write("\n\t\t\tmax_strength = %s"%module.mp_max_strength)
        if module.mp_armor_value != 0:
            moduleGroup.write("\n\t\t\tarmor_value = %s"%module.mp_armor_value)
        moduleGroup.write("\n\t\t}")

        #build_cost_resources
        if module.res_steel != 0 or module.res_chromium != 0:
            moduleGroup.write("\n\t\tbuild_cost_resources = {")
            if module.res_steel != 0:
                moduleGroup.write("\n\t\t\tsteel = %s"%module.res_steel)
            if module.res_chromium != 0:
                moduleGroup.write("\n\t\t\tchromium = %s"%module.res_chromium)
            moduleGroup.write("\n\t\t}")
        
        j=1
        #can_convert_from
        if True:
            convertDiscount = 0.85
            if "capital" in module.name:
                #upto 2x4 3x3 4x2  
                if "2x" in module.name:
                    # a3x2_2x1
                    moduleGroup.write("\n\t\tcan_convert_from = {")
                    moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-11],"a3x1_2x1"))
                    moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount- module.ic_one_turret*2))
                    moduleGroup.write("\n\t\t}")
                    # a4x2_2x1
                    moduleGroup.write("\n\t\tcan_convert_from = {")
                    moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-11],"a4x1_2x1"))
                    moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*2))
                    moduleGroup.write("\n\t\t}")
                    while j <= 4:
                        moduleGroup.write("\n\t\tcan_convert_from = {")
                        moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-9],j))
                        if j <= int(module.name[-9]):
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*j))
                        else:
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*int(module.name[-9])))
                        moduleGroup.write("\n\t\t}")
                        j +=1
                elif "3x" in module.name:
                    # a3x2_2x1
                    moduleGroup.write("\n\t\tcan_convert_from = {")
                    moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-11],"a3x1_2x1"))
                    moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*3))
                    moduleGroup.write("\n\t\t}")
                    while j <= 3:
                        moduleGroup.write("\n\t\tcan_convert_from = {")
                        moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-9],j))
                        if j <= int(module.name[-9]):
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic - module.ic_one_turret*j))
                        else:
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic - module.ic_one_turret*int(module.name[-9])))
                        moduleGroup.write("\n\t\t}")
                        j +=1
                elif "4x" in module.name:
                    # a4x2_2x1
                    moduleGroup.write("\n\t\tcan_convert_from = {")
                    moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-11],"a4x1_2x1"))
                    moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*4))
                    moduleGroup.write("\n\t\t}")
                    while j <= 2:
                        moduleGroup.write("\n\t\tcan_convert_from = {")
                        moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-9],j))
                        if j <= int(module.name[-9]):
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic - module.ic_one_turret*j))
                        else:
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic - module.ic_one_turret*int(module.name[-9])))
                        moduleGroup.write("\n\t\t}")
                        j +=1
            elif "cruiser" in module.name:  #upto 2x4 3x3 4x2
                if "2x" in module.name:
                    while j <= 4:
                        moduleGroup.write("\n\t\tcan_convert_from = {")
                        moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-9],j))
                        if j <= int(module.name[-9]):
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*j))
                        else:
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*int(module.name[-9])))
                        moduleGroup.write("\n\t\t}")
                        j +=1
                elif "3x" in module.name:
                    while j <= 3:
                        moduleGroup.write("\n\t\tcan_convert_from = {")
                        moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-9],j))
                        if j <= int(module.name[-9]):
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*j))
                        else:
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*int(module.name[-9])))
                        moduleGroup.write("\n\t\t}")
                        j +=1
                elif "4x" in module.name:
                    while j <= 2:
                        moduleGroup.write("\n\t\tcan_convert_from = {")
                        moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-9],j))
                        if j <= int(module.name[-9]):
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*j))
                        else:
                            moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_turret*int(module.name[-9])))
                        moduleGroup.write("\n\t\t}")
                        j +=1
                elif True: #turrets are more of an abstraction.
                    j=2
                    while j<=9:
                        if j==7 or j==8:
                            pass
                        else:
                            moduleGroup.write("\n\t\tcan_convert_from = {")
                            moduleGroup.write("\n\t\t\tmodule = %sx0%g"%(module.name[:-11],j))
                            if j<=module.numberGuns:
                                moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_gun*j))
                            else:
                                moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_gun * module.numberGuns))
                            moduleGroup.write("\n\t\t}")
                        j+=1
                elif False: #turret distinctions are important
                    if module.numberGuns == 2 or module.numberGuns == 4:     #x04 x06 x08 x10
                        j=4
                        while j <= 6:
                            moduleGroup.write("\n\t\tcan_convert_from = {")
                            if j<10:
                                moduleGroup.write("\n\t\t\tmodule = %s0%s"%(module.name[:-10],j))
                            else:
                                moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-10],j))
                            if j<=module.numberGuns:
                                moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_gun*j))
                            else:
                                moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_gun * module.numberGuns))
                            moduleGroup.write("\n\t\t}")
                            j+=2
                    if module.numberGuns == 3 or module.numberGuns == 6:     # x09 x12 x15
                        j = 9
                        while j <= 9:
                            moduleGroup.write("\n\t\tcan_convert_from = {")
                            if j<10:
                                moduleGroup.write("\n\t\t\tmodule = %s0%s"%(module.name[:-10],j))
                            else:
                                moduleGroup.write("\n\t\t\tmodule = %s%s"%(module.name[:-10],j))
                            if j<=module.numberGuns:
                                moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_gun*j))
                            else:
                                moduleGroup.write("\n\t\t\tconvert_cost_ic = %g"%(module.add_build_cost_ic*convertDiscount - module.ic_one_gun * module.numberGuns))
                            moduleGroup.write("\n\t\t}")
                            j +=3

        moduleGroup.write("\n\t\tcritical_parts = { %s }"%module.critical_parts)
        moduleGroup.write("\n\t\tdismantle_cost_ic = %s"%module.dismantle_cost_ic)

        moduleGroup.write("\n\n\t}")

        #Module Icons
        gfx_moduleGroup.write("\n\tspriteType = {")
        gfx_moduleGroup.write("\n\t\tname = \"GFX_SMI_%s\""%module.name)
        gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_flightdeck_")
        if "_AHL_" in module.name:
            gfx_moduleGroup.write("a")
        gfx_moduleGroup.write("%s.dds\""%module.name[-2:])
        gfx_moduleGroup.write("\n\t}\n")

        #Ship sub-Unit
        Sub_UnitModule.write("\n%s = 1"%module.name)

    gfx_moduleGroup.write("\n}")
    moduleGroup.write("\n}")
    moduleGroup.close()

def Module_sub_outputer(module_array, file):
    tmpfile = file.split("\\")
    #print(tmpfile[len(tmpfile)-1])
    #print(tmpfile[:(tmpfile[len(tmpfile)-1].find("."))])
    moduleGroup = open(file, "w")
    gfx_moduleGroup = open("Output\\interface\\%s_.gfx"%tmpfile[len(tmpfile)-1][:(tmpfile[len(tmpfile)-1].find("."))], "w")
    Sub_UnitModule = open("Output\\_module lists\\%s_Sub-Unit.txt"%tmpfile[len(tmpfile)-1][:(tmpfile[len(tmpfile)-1].find("."))], "w") 
    Sub_UnitModule_Cruiser = open("Output\\_module lists\\%s_cruiser_Sub-Unit.txt"%tmpfile[len(tmpfile)-1][:(tmpfile[len(tmpfile)-1].find("."))], "w")

    moduleGroup.write("equipment_modules = {\n")
    gfx_moduleGroup.write("spriteTypes = {\n")
    for module in module_array:
        moduleGroup.write("\n\t%s = {"%module.name)
        moduleGroup.write("\n\t\tcategory = %s"%module.category)
        if module.gui_category != "" and not module.gui_category is module.category:
            moduleGroup.write("\n\t\tgui_category = %s"%module.gui_category)
        moduleGroup.write("\n\t\tsfx = sfx_ui_sd_module_turret")

        if module.parent != "":
            moduleGroup.write("\n\t\tparent = %s"%module.parent)

        moduleGroup.write("\n\n\t\tmanpower = %d"%module.manpower)
        #add_stats
        moduleGroup.write("\n\t\tadd_stats = {")
        moduleGroup.write("\n\t\t\tbuild_cost_ic = %s"%module.add_build_cost_ic)
        moduleGroup.write("\n\t\t\tmax_strength = %s"%module.add_max_strength)
        if float(module.add_max_strength)<0.001:
            print(module)
            print("\t%s"%module.add_max_strength)
            print("\t%f"%module.add_max_strength)
            print()
        if module.add_hg_attack != 0:
            moduleGroup.write("\n\t\t\thg_attack = %s"%module.add_hg_attack)
        if module.add_lg_attack != 0:
            moduleGroup.write("\n\t\t\tlg_attack = %s"%module.add_lg_attack)
        if module.add_anti_air_attack != 0:
            moduleGroup.write("\n\t\t\tanti_air_attack = %s"%module.add_anti_air_attack)
        moduleGroup.write("\n\t\t\tsupply_consumption = %s"%module.add_supply_consumption)
        moduleGroup.write("\n\t\t\tsurface_visibility = %s"%module.add_surface_visibility)
        moduleGroup.write("\n\t\t\tsub_visibility = %s"%module.add_sub_visibility)
        moduleGroup.write("\n\t\t}")

        #add_average_stats
        moduleGroup.write("\n\t\tadd_average_stats = {")
        if module.av_hg_armor_piercing != 0:
            moduleGroup.write("\n\t\t\thg_armor_piercing = %s"%module.av_hg_armor_piercing)
        if module.av_lg_armor_piercing != 0:
            moduleGroup.write("\n\t\t\tlg_armor_piercing = %s"%module.av_lg_armor_piercing)
        moduleGroup.write("\n\t\t}")

        #multiply_stats
        moduleGroup.write("\n\t\tmultiply_stats = {")
        moduleGroup.write("\n\t\t\tbuild_cost_ic = %s"%module.mp_build_cost_ic)
        moduleGroup.write("\n\t\t\treliability = %s"%module.mp_reliability)
        if float(module.mp_reliability)>-.0001:
            print(module)
            print("\t%s"%module.mp_reliability)
            print("\t%f"%module.mp_reliability)
            print()
        moduleGroup.write("\n\t\t\tnaval_speed = %s"%module.mp_naval_speed)
        moduleGroup.write("\n\t\t\tfuel_consumption = %s"%module.mp_fuel_consumption)
        if module.mp_max_strength != 0:
            moduleGroup.write("\n\t\t\tmax_strength = %s"%module.mp_max_strength)
        if module.mp_armor_value != 0:
            moduleGroup.write("\n\t\t\tarmor_value = %s"%module.mp_armor_value)
        moduleGroup.write("\n\t\t}")

        #build_cost_resources
        if module.res_steel != 0 or module.res_chromium != 0:
            moduleGroup.write("\n\t\tbuild_cost_resources = {")
            if module.res_steel != 0:
                moduleGroup.write("\n\t\t\tsteel = %s"%module.res_steel)
            if module.res_chromium != 0:
                moduleGroup.write("\n\t\t\tchromium = %s"%module.res_chromium)
            moduleGroup.write("\n\t\t}")

        moduleGroup.write("\n\t\tcritical_parts = { ")
        if module.caliber < 8:
            moduleGroup.write("damaged_light_guns }")
        else:
            moduleGroup.write("damaged_heavy_guns }")

        moduleGroup.write("\n\t\tdismantle_cost_ic = %g"%module.dismantle_cost_ic)

        moduleGroup.write("\n\t}")
        #Module Icons       figgure this out
        gfx_moduleGroup.write("\n\tspriteType = {")
        gfx_moduleGroup.write("\n\t\tname = \"GFX_SMI_%s\""%module.name)
        if module.dualPurpse:
            gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_cruiser_dp_")
            if module.caliber >5.9:
                gfx_moduleGroup.write("heavy_")
            gfx_moduleGroup.write("battery_%g.dds\""%module.numberGuns)
        else:
            if module.caliber <10:
                gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_")
                if module.caliber >5.9:
                    gfx_moduleGroup.write("cruiser_heavy_")
                else:
                    gfx_moduleGroup.write("dd_")
            else:
                gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_capital_")

            gfx_moduleGroup.write("battery_%g.dds\""%module.numberGuns)
        gfx_moduleGroup.write("\n\t}\n")

        #Ship sub-Unit
        Sub_UnitModule.write("\n%s = 1"%module.name)
        if module.caliber>7:
            Sub_UnitModule_Cruiser.write("\t"*4)
            Sub_UnitModule_Cruiser.write("%s = 1\n"%module.name)



    gfx_moduleGroup.write("\n}")
    moduleGroup.write("\n}")
    moduleGroup.close()
    Sub_UnitModule_Cruiser.close()
    Sub_UnitModule.close()

def Module_Guns_outputer(module_array, file):
    moduleGroup = open(file, "w")
    tmpfile = file.split("\\")
    #print(tmpfile[len(tmpfile)-1])
    #print(tmpfile[:(tmpfile[len(tmpfile)-1].find("."))])

    gfx_moduleGroup = open("Output\\interface\\%s_.gfx"%tmpfile[len(tmpfile)-1][:(tmpfile[len(tmpfile)-1].find("."))], "w")
    Sub_UnitModule = open("Output\\_module lists\\%s_Sub-Unit.txt"%tmpfile[len(tmpfile)-1][:(tmpfile[len(tmpfile)-1].find("."))], "w")  

    #print(gfx_moduleGroup.name)

    moduleGroup.write("equipment_modules = {\n")
    gfx_moduleGroup.write("spriteTypes = {\n")

    for module in module_array:
        if "3x1_2" in module.name or "4x1_2" in module.name:
            moduleGroup.write("\n\t%s = {"%(module.name[:module.name.find("x1_2")-1] + "a" + module.name[module.name.find("x1_2")-1:]))
            #print(module.name[:module.name.find("x1_2")-1] + "a" + module.name[module.name.find("x1_2")-1:])
        else:
            moduleGroup.write("\n\t%s = {"%module.name)
        moduleGroup.write("\n\t\tcategory = %s"%module.category)
        moduleGroup.write("\n\t\tgui_category = %s"%module.gui_category)
        moduleGroup.write("\n\t\tsfx = sfx_ui_sd_module_turret")
        
        if module.parent != "":
            moduleGroup.write("\n\t\tparent = %s"%module.parent)

        if module.add_equipment_type != "":
            moduleGroup.write("\n\n\t\tadd_equipment_type = %s"%module.add_equipment_type)

        moduleGroup.write("\n\n\t\tmanpower = %d"%module.manpower)
        #add_stats
        moduleGroup.write("\n\t\tadd_stats = {")
        moduleGroup.write("\n\t\t\tbuild_cost_ic = %s"%module.add_build_cost_ic)
        moduleGroup.write("\n\t\t\tmax_strength = %s"%module.add_max_strength)
        if module.add_hg_attack != 0:
            moduleGroup.write("\n\t\t\thg_attack = %s"%module.add_hg_attack)
        if module.add_lg_attack != 0:
            moduleGroup.write("\n\t\t\tlg_attack = %s"%module.add_lg_attack)
        if module.add_anti_air_attack != 0:
            moduleGroup.write("\n\t\t\tanti_air_attack = %s"%module.add_anti_air_attack)
        moduleGroup.write("\n\t\t\tsupply_consumption = %s"%module.add_supply_consumption)
        moduleGroup.write("\n\t\t\tsurface_visibility = %s"%module.add_surface_visibility)
        moduleGroup.write("\n\t\t}")

        #add_average_stats
        moduleGroup.write("\n\t\tadd_average_stats = {")
        if module.av_hg_armor_piercing != 0:
            moduleGroup.write("\n\t\t\thg_armor_piercing = %s"%module.av_hg_armor_piercing)
        if module.av_lg_armor_piercing != 0:
            moduleGroup.write("\n\t\t\tlg_armor_piercing = %s"%module.av_lg_armor_piercing)
        moduleGroup.write("\n\t\t}")

        #multiply_stats
        moduleGroup.write("\n\t\tmultiply_stats = {")
        moduleGroup.write("\n\t\t\tbuild_cost_ic = %s"%module.mp_build_cost_ic)
        moduleGroup.write("\n\t\t\treliability = %s"%module.mp_reliability)
        moduleGroup.write("\n\t\t\tnaval_speed = %s"%module.mp_naval_speed)
        moduleGroup.write("\n\t\t\tfuel_consumption = %s"%module.mp_fuel_consumption)
        if module.mp_max_strength != 0:
            moduleGroup.write("\n\t\t\tmax_strength = %s"%module.mp_max_strength)
        if module.mp_armor_value != 0:
            moduleGroup.write("\n\t\t\tarmor_value = %s"%module.mp_armor_value)
        moduleGroup.write("\n\t\t}")

        #build_cost_resources
        if module.res_steel != 0 or module.res_chromium != 0:
            moduleGroup.write("\n\t\tbuild_cost_resources = {")
            if module.res_steel != 0:
                moduleGroup.write("\n\t\t\tsteel = %s"%module.res_steel)
            if module.res_chromium != 0:
                moduleGroup.write("\n\t\t\tchromium = %s"%module.res_chromium)
            moduleGroup.write("\n\t\t}")

        moduleGroup.write("\n\t\tcritical_parts = { %s }"%module.critical_parts)
        moduleGroup.write("\n\t\tdismantle_cost_ic = %s"%module.dismantle_cost_ic)
        moduleGroup.write("\n\n\t}")

        #Module Icons
        gfx_moduleGroup.write("\n\tspriteType = {")
        gfx_moduleGroup.write("\n\t\tname = \"GFX_SMI_")
        if "3x1_2" in module.name:    # a3x2_2x1
            #print(module.name[:module.name.find("3x1_")] + "a" + module.name[module.name.find("3x1_"):])
            gfx_moduleGroup.write("%sa%s\""%(module.name[:module.name.find("3x1_")],module.name[module.name.find("3x1_"):]))
        elif "4x1_2" in module.name:    # a4x2_2x1
            gfx_moduleGroup.write("%sa%s\""%(module.name[:module.name.find("4x1_")],module.name[module.name.find("4x1_"):]))
        else:
            gfx_moduleGroup.write("%s\""%module.name)

        if module.caliber > 10:
            gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_capital_battery_")
            if "3x1_2" in module.name:    # a3x2_2x1
                gfx_moduleGroup.write("3x1_2x1.dds\"")
            elif "4x1_2" in module.name:    # a4x2_2x1
                gfx_moduleGroup.write("4x1_2x1.dds\"")
            else:
                gfx_moduleGroup.write("%gx%g.dds\""%(int(module.numberGuns/module.numberTurrets), int(module.numberTurrets)))

        elif module.dualPurpse and module.caliber > 5.9:
            gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_cruiser_dp_heavy_battery_%g.dds\""%module.numberGuns)
        elif module.dualPurpse:
            gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_cruiser_dp_battery_%g.dds\""%module.numberGuns)
        elif module.caliber > 5.9:
            gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_cruiser_heavy_battery_%g.dds\""%module.numberGuns)
        else:
            gfx_moduleGroup.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/modules/icons/nrm_cruiser_battery_%g.dds\""%module.numberGuns)

        gfx_moduleGroup.write("\n\t}\n")

        #Ship sub-Unit
        Sub_UnitModule.write("\n%s = 1"%module.name)

    gfx_moduleGroup.write("\n}")
    moduleGroup.write("\n}")
    moduleGroup.close()

def Module_deckgun_outputer(module_array, file):
    tmpfile = file.split("\\")
    moduleGroup = open(file, "w")
    moduleGroup.write("equipment_modules = {")
    for module in module_array:
        moduleGroup.write("\n\t%s = {"%module.name)
        moduleGroup.write("\n\t\tcategory = %s"%module.category)
        if module.gui_category != "" and not module.gui_category is module.category:
            moduleGroup.write("\n\t\tgui_category = %s"%module.gui_category)
        moduleGroup.write("\n\t\tsfx = sfx_ui_sd_module_turret")
        if module.parent != "":
            moduleGroup.write("\n\t\tparent = %s"%module.parent)

        moduleGroup.write("\n\n\t\tmanpower = %d"%module.manpower)
        #add_stats
        moduleGroup.write("\n\t\tadd_stats = {")
        moduleGroup.write("\n\t\t\tbuild_cost_ic = %s"%module.add_build_cost_ic)
        moduleGroup.write("\n\t\t\tmax_strength = %s"%module.add_max_strength)
        if module.add_hg_attack != 0:
            moduleGroup.write("\n\t\t\thg_attack = %s"%module.add_hg_attack)
        if module.add_lg_attack != 0:
            moduleGroup.write("\n\t\t\tlg_attack = %s"%module.add_lg_attack)
        if module.add_anti_air_attack != 0:
            moduleGroup.write("\n\t\t\tanti_air_attack = %s"%module.add_anti_air_attack)
        moduleGroup.write("\n\t\t\tsupply_consumption = %s"%module.add_supply_consumption)
        moduleGroup.write("\n\t\t\tsurface_visibility = %s"%module.add_surface_visibility)
        moduleGroup.write("\n\t\t\tsub_visibility = %s"%module.add_sub_visibility)
        moduleGroup.write("\n\t\t}")

        #add_average_stats
        moduleGroup.write("\n\t\tadd_average_stats = {")
        if module.av_hg_armor_piercing != 0:
            moduleGroup.write("\n\t\t\thg_armor_piercing = %s"%module.av_hg_armor_piercing)
        if module.av_lg_armor_piercing != 0:
            moduleGroup.write("\n\t\t\tlg_armor_piercing = %s"%module.av_lg_armor_piercing)
        moduleGroup.write("\n\t\t}")

        #multiply_stats
        moduleGroup.write("\n\t\tmultiply_stats = {")
        moduleGroup.write("\n\t\t\tbuild_cost_ic = %s"%module.mp_build_cost_ic)
        moduleGroup.write("\n\t\t\treliability = %s"%module.mp_reliability)
        moduleGroup.write("\n\t\t\tnaval_speed = %s"%module.mp_naval_speed)
        moduleGroup.write("\n\t\t\tfuel_consumption = %s"%module.mp_fuel_consumption)
        if module.mp_max_strength != 0:
            moduleGroup.write("\n\t\t\tmax_strength = %s"%module.mp_max_strength)
        if module.mp_armor_value != 0:
            moduleGroup.write("\n\t\t\tarmor_value = %s"%module.mp_armor_value)
        moduleGroup.write("\n\t\t}")

        #build_cost_resources
        if module.res_steel != 0 or module.res_chromium != 0:
            moduleGroup.write("\n\t\tbuild_cost_resources = {")
            if module.res_steel != 0:
                moduleGroup.write("\n\t\t\tsteel = %s"%module.res_steel)
            if module.res_chromium != 0:
                moduleGroup.write("\n\t\t\tchromium = %s"%module.res_chromium)
            moduleGroup.write("\n\t\t}")

        moduleGroup.write("\n\t\tcritical_parts = { ")
        if module.caliber < 8:
            moduleGroup.write("damaged_light_guns }")
        else:
            moduleGroup.write("damaged_heavy_guns }")

        if not module.dismantle_cost_ic ==0:
            moduleGroup.write("\n\t\tdismantle_cost_ic = %g"%module.dismantle_cost_ic)

        moduleGroup.write("\n\t}")

    moduleGroup.close()
    pass

def Tech_outputer(tech_set, file):
    techGroup = open(file, "w")
    techGroup.write("technologies = {\n")

    for tech,modules in tech_set.items():
        techGroup.write("\n\t%s = {"%tech)
        techGroup.write("\n\t\tenable_equipment_modules = {")
        for module in modules:
            techGroup.write("\n\t\t\t%s"%module)
        techGroup.write("\n\t\t}")
        techGroup.write("\n\t\tai_will_do = {")
        techGroup.write("\n\t\t\tfactor = 0")
        techGroup.write("\n\t\t}")
        techGroup.write("\n\t}")

    techGroup.write("\n}")
    techGroup.close()

def Event_outputer(techEvents, file, flag, namespace):
    i=1
    eventGroup = open(file, "w")
    eventGroup.write("\nadd_namespace = %s\n"%namespace)
    
    eventHandout = open(file.replace(".","_Handout."), "w")
    eventHandout.write("\nadd_namespace = %s_handout\n"%namespace)
    eventHandout.write("\ncountry_event = {")
    eventHandout.write("\n\tid = %s_handout.%d"%(namespace,i))
    eventHandout.write("\n\ttitle = %s_handout.%d.t"%(namespace,i))
    eventHandout.write("\n\tdesc = %s_handout.%d.desc"%(namespace,i))
    eventHandout.write("\n\thidden = yes")
    eventHandout.write("\n\tis_triggered_only = yes")
    eventHandout.write("\n\n\timmediate = {")

    for tech in techEvents:
        eventGroup.write("\n#%s"%tech.name)
        eventGroup.write("\ncountry_event = {")
        eventGroup.write("\n\tid = %s.%d"%(namespace,i))
        eventGroup.write("\n\ttitle = %s.%d.t"%(namespace,i))
        eventGroup.write("\n\tdesc = %s.%d.desc"%(namespace,i))
        eventGroup.write("\n\thidden = yes")

        eventGroup.write("\n\ttrigger = {")
        eventGroup.write("\n\t\thas_country_flag = %s"%flag)
        eventGroup.write("\n\t\tnot = { has_tech = %s } "%tech.name)
        if tech.gunTech.find("|") >-1:
            eventGroup.write("\n\t\tor = {")
            eventGroup.write("\n\t\t\thas_tech = %s"%tech.gunTech.partition("|")[0])
            eventGroup.write("\n\t\t\thas_tech = %s"%tech.gunTech.partition("|")[2])
            eventGroup.write("\n\t\t }")
        else:
            eventGroup.write("\n\t\thas_tech = %s"%tech.gunTech)
        if tech.launcherTech != "":
            eventGroup.write("\n\t\thas_tech = %s"%tech.launcherTech)
        if tech.hangerTech != "":
            eventGroup.write("\n\t\thas_tech = %s"%tech.hangerTech)
        if not tech.treatyCompliant:
            eventGroup.write("\n\t\tnot = { has_idea = MTG_naval_treaty_adherent }")

        eventGroup.write("\n\t}")

        eventGroup.write("\n\tmean_time_to_happen = {")
        eventGroup.write("\n\t\tdays = 0")
        eventGroup.write("\n\t}")
        eventGroup.write("\n\timmediate = {")
        eventGroup.write("\n\t\tset_technology = { %s = 1 }"%tech.name)
        eventGroup.write("\n\t}")
        eventGroup.write("\n}")

        #handout event
        eventHandout.write("\n\t\tif = {")
        eventHandout.write("\n\t\t\tlimit = {")
        if "|" in tech.gunTech:
            eventHandout.write("\n\t\t\t\tor = {")
            eventHandout.write("\n\t\t\t\t\thas_tech = %s"%tech.gunTech.partition("|")[0])
            eventHandout.write("\n\t\t\t\t\thas_tech = %s"%tech.gunTech.partition("|")[2])
            eventHandout.write("\n\t\t\t\t}")
        else:
            eventHandout.write("\n\t\t\t\thas_tech = %s"%tech.gunTech)
        if tech.launcherTech != "":
            eventHandout.write("\n\t\t\t\thas_tech = %s"%tech.launcherTech)
        if tech.hangerTech != "":
            eventHandout.write("\n\t\t\t\thas_tech = %s"%tech.hangerTech)
        if not tech.treatyCompliant:
            eventHandout.write("\n\t\t\t\tnot = { has_idea = MTG_naval_treaty_adherent }")

        eventHandout.write("\n\t\t\t}")
        eventHandout.write("\n\t\t\tset_technology = { popup = no %s = 1 }"%tech.name)
        eventHandout.write("\n\t\t}")
       
        i += 1
    eventHandout.write("\n\t}")
    eventHandout.write("\n}")
    eventGroup.close()
    eventHandout.close()

def local_ship_modules_local(module_set, file):
    localModule = open(file, "w", encoding='utf-8-sig')
    localModule.write("l_english:\n")
    gunlocal = ""

    techLevel = ["", "(Early)", "(Interwar)", "(Advanced)", "(Rapid Fire)"]
    turrets = ["","","Twin","Triple","Quad"]

    sourceFileList = glob.glob("Input\\localisation\\*.yml")
    
    print("English localization")
    for filelist in sourceFileList:
        if "_l_english" in filelist:
            #print(filelist)
            nation = filelist[filelist.find("english")+8: filelist.find(".yml")]
            print(nation)
            for module in module_set:
                source_guns = open(filelist ,"r+", encoding='utf-8-sig' )
                for line in source_guns:
                    if not line.strip()  or "_desc" in line:
                        continue
                    else:
                        #get name used for national/default gun by calliber
                        moduleKey = ""
                        if ("DP_5_2_x03" in module.name and "DP_5_2_x3" in line) or ("DP_5_2_x06" in module.name and "DP_5_2_x6" in line):
                            moduleKey = "DP_5_2_"
                        elif "battery" in module.name:
                            moduleKey = module.name[module.name.find("battery"):module.name.find("x")-1]
                        elif "deckgun" in module.name:
                            moduleKey = module.name[module.name.find("submarine"):module.name.find("x")-1]

                        if moduleKey in line:
                            if "battery" in module.name:
                                gunlocal =line[line.find("\"")+1:line.find("(")]
                            elif "deckgun" in module.name:
                                gunlocal =line[line.find("\"")+1:len(line.strip())]
                            #print(gunlocal)
                            #print(moduleKey)
                            
                            break
                localModule.write("\n ")
                #add country prefix if it exists
                if nation:
                    localModule.write("%s_"%nation)
                #write module name as it apperse in game code
                if "x1_2x" in module.name:
                    localModule.write("%sa%s:0 \""%(module.name[:module.name.find("x1_2")-1],module.name[module.name.find("x1_2")-1:]))
                else:
                    localModule.write("%s:0 \""%module.name)
                localModule.write(gunlocal)
                localModule.write("%s "%techLevel[module.level])
                if "deckgun" in module.name:
                    localModule.write("(%s-gun Superfiring)"%module.numberGuns)
                else:
                    #check to see if it is not a hybrid module
                    if module.add_carrier_size ==0:
                        localModule.write("%i-gun "%module.numberGuns)
                    #check to see if it is dual purpose / main battery
                    if module.dualPurpse:
                        localModule.write("Dual Purpose")
                    else:
                        localModule.write("Main")
                    localModule.write(" Battery")
                #add aircraft numbers and armor type for hybrid modules
                if module.add_carrier_size >0:
                    localModule.write(" (%d Aircraft"%module.add_carrier_size)
                    if module.name.find("_AHL_") >-1:
                        localModule.write(" Armored)")
                    else:
                        localModule.write(")")
                #add submersable tag for sub gun batteries
                elif module.add_sub_visibility >0:
                    localModule.write(" (Submersible)")
                #special cases for mixed battery turret arangment
                elif "x1_2x" in module.name:
                    if "3x" in module.name:
                        localModule.write(" (1x Triple, 1x Twin)")
                    elif "4x" in module.name:
                        localModule.write(" (1x Quad, 1x Twin)")
                #discribe capital ship turret arangment 
                elif module.caliber > 9:
                    localModule.write(" (%gx %s)"%(int(module.name[len(module.name)-1]) , turrets[int(module.numberGuns/module.numberTurrets)]))
                localModule.write("\"")
            localModule.write("\n")

    for module in module_set:
        localModule.write("\n %s_desc:0 \"\""%module.name)

    category_list = []
    for module in module_set:
        if "submarine" in module.name:
            pass
        else:
            if not module.category in category_list:
                #print(module.category)
                category_list.append(module.category)
                localModule.write("\n EQ_MOD_CAT_%s_TITLE:0 \"\""%module.category)
                localModule.write("\n EQ_MOD_CAT_%s_long_TITLE:0 \"\""%module.category)
    
i=0

def local_ship_modules_local_ger(module_set, file):
    localModule = open(file, "w", encoding='utf-8-sig')
    localModule.write("l_german:\n")
    gunlocal = ""

    techLevel = ["", "(Früh)", "(Zwischenkriegszeit)", "(Fortschrittlich)", "(Schnellfeuer)"]
    turrets = ["","","Twin","Triple","Quad"]

    sourceFileList = glob.glob("Input\\localisation\\*.yml")

    print("German localization")
    for filelist in sourceFileList:
        if "_l_english" in filelist:
            #print(filelist)
            nation = filelist[filelist.find("english")+8: filelist.find(".yml")]
            print(nation)
            for module in module_set:
                source_guns = open(filelist ,"r+", encoding='utf-8-sig' )
                for line in source_guns:
                    if not line.strip()  or "_desc" in line:
                        continue
                    else:
                        #get name used for national/default gun by calliber
                        moduleKey = ""
                        if ("DP_5_2_x03" in module.name and "DP_5_2_x3" in line) or ("DP_5_2_x06" in module.name and "DP_5_2_x6" in line):
                            moduleKey = "DP_5_2_"
                        elif "battery" in module.name:
                            moduleKey = module.name[module.name.find("battery"):module.name.find("x")-1]
                        elif "deckgun" in module.name:
                            moduleKey = module.name[module.name.find("submarine"):module.name.find("x")-1]
                        if moduleKey in line:
                            if "battery" in module.name:
                                gunlocal =line[line.find("\"")+1:line.find("(")]
                            elif "deckgun" in module.name:
                                gunlocal =line[line.find("\"")+1:len(line.strip())]
                            #print(gunlocal)
                            break
                localModule.write("\n ")
                #add country prefix if it exists
                if nation:
                    localModule.write("%s_"%nation)
                #write module name as it apperse in game code
                if "x1_2x" in module.name:
                    localModule.write("%sa%s:0 \""%(module.name[:module.name.find("x1_2")-1],module.name[module.name.find("x1_2")-1:]))
                else:
                    localModule.write("%s:0 \""%module.name)
                localModule.write(gunlocal)
                localModule.write("%s "%techLevel[module.level])
                if "deckgun" in module.name:
                    localModule.write("(%s-gun Superfeuer)"%module.numberGuns)
                else:
                    #check to see if it is not a hybrid module
                    if module.add_carrier_size ==0:
                        localModule.write("%i-gun "%module.numberGuns)
                    #check to see if it is dual purpose / main battery
                    if module.dualPurpse:
                        localModule.write("Mehrzweck-Geschütz")
                    else:
                        localModule.write("Hauptgeschütz")
                #add aircraft numbers and armor type for hybrid modules
                if module.add_carrier_size >0:
                    localModule.write(" (%d Kapazität"%module.add_carrier_size)
                    if module.name.find("_AHL_") >-1:
                        localModule.write(" Gepanzerter)")
                    else:
                        localModule.write(" Umgebauter)")
                #add submersable tag for sub gun batteries
                elif module.add_sub_visibility >0:
                    localModule.write(" (Unterseeisch)")
                #special cases for mixed battery turret arangment
                elif "x1_2x" in module.name:
                    if "3x" in module.name:
                        localModule.write(" (1x Triple, 1x Twin)")
                    elif "4x" in module.name:
                        localModule.write(" (1x Quad, 1x Twin)")
                #discribe capital ship turret arangment 
                elif module.caliber > 9:
                    localModule.write(" (%gx %s)"%(int(module.name[len(module.name)-1]) , turrets[int(module.numberGuns/module.numberTurrets)]))
                localModule.write("\"")
            localModule.write("\n")

    for module in module_set:
        localModule.write("\n %s_desc:0 \"\""%module.name)

    category_list = []
    for module in module_set:
        if "submarine" in module.name:
            pass
        else:
            if not module.category in category_list:
                #print(module.category)
                category_list.append(module.category)
                localModule.write("\n EQ_MOD_CAT_%s_TITLE:0 \"\""%module.category)
i=0

def local_tech(tech_set, file):
    techGroup = open(file, "w", encoding='utf-8-sig')
    techGroup.write("l_english:\n")

    for tech,module in tech_set.items():
        #print(tech)
        techGroup.write("\n %s:0 \""%tech)
        tmpLine = tech.replace("5h","5.5").replace("nrm_battery_","").replace("_", " ")
        line2 = ""
        for word in tmpLine.split(" "):
            if word.isnumeric() or "." in word:
                #print(word)
                line2 += word + "in "
            elif "dp" in word:
                line2 += "dual purpose "
            else:
                line2 += word + " "
        #print(line2)
        #techGroup.write("%s\""%tech.replace("5h","5.5").replace("nrm_","").replace("_", " "))
        techGroup.write("%s\""%line2.strip())
    techGroup.write("\n")
    for tech,module in tech_set.items():
        techGroup.write("\n %s_desc:0 \"\""%tech)
    techGroup.close()

    filegfx = "output\\interface\\" + file.lstrip("Output\\localisation\\english\\").rstrip("_l_english.yml") + ".gfx"
    techgfx = open(filegfx, "w", encoding='utf-8')
    #print(techgfx.name)
    techgfx.write("spriteTypes = {")
    for tech in tech_set:
        
        techgfx.write("\n\tSpriteType = {")
        techgfx.write("\n\t\tname = \"GFX_%s_medium\""%tech)
        techgfx.write("\n\t\ttexturefile = \"") 
        if "converted" in tech or "armored" in tech:
            techgfx.write("gfx/interface/equipmentdesigner/modules/icons/nrm_flightdeck.dds")
        elif "submarine_turret" in tech:
            techgfx.write("gfx/interface/technologies/")
            if "modern_" in tech:
                techgfx.write("modern_")
            elif "_4_" in tech or "_5_" in tech or "advanced_medium" in tech:
                techgfx.write("advanced_")
            elif "_2_" in tech or "_3_" in tech:
                techgfx.write("improved_")
            else:
                techgfx.write("basic_")
            if "light_battery" in tech:
                techgfx.write("light_battery")
            elif "medium_battery" in tech:
                techgfx.write("medium_battery")
            else:
                techgfx.write("heavy_battery")
            techgfx.write(".dds")
            #print(tech)
        else:
            techgfx.write("\"")
        techgfx.write("\"\n\t}")
    techgfx.write("\n}")

def local_tech_ger(tech_set, file, gun, hanger, launcer):
    techGroup = open(file, "w", encoding='utf-8-sig')
    techGroup.write("l_german:\n")

    gun_tech_list_ger = ["Grundbatterie", "Verbesserte 115-135mm Batterie", "Fortschrittliche 115-135mm Batterie", "Mehrzweck 115-135mm Batterie", "Fortschrittliche Mehrzweck 115-135mm Batterie", "Verbessertes 135-160mm Geschütz", "Fortschrittliches 135-160mm Geschütz", "Schnellfeuer 145-160mm Batterie", "Mehrzweck 135-145mm Batterie", "Fortschrittliche Mehrzweck 135-145mm Batterie", "Mehrzweck 145-160mm Batterie", "180-210mm Batterie", "Verbesserte 180-210mm Batterie", "Fortschrittliche 180-210mm Batterie", "Schnellfeuer 180-210mm Batterie", "Verbessertes 250-310mm Geschütz", "Fortschrittliches 250-310mm Geschütz", "320-360mm Batterie", "Verbesserte 320-360mm Batterie", "Fortschrittliche 320-360mm Batterie", "380-420mm Batterie", "Verbesserte 380-420mm Batterie", "Fortschrittliche 380-420mm Batterie", "Verbesserte 450-480mm Batterie", "Fortschrittliche 450-480mm Batterie", "Verbesserte 500-520mm Batterie", "Fortschrittliche 500-520mm Batterie"]
    hanger_tech_list_ger = ["Umgebaute ", "Gepanzert"]
    launcher_tech_list_ger = ["Klein", "Mittel", "Groß"]
    
    for tech,module in tech_set.items():
        techGroup.write("\n %s:0 \""%tech)
        x=0
        y=0
        z=0
        for name in gun:
            if name in tech:
                #print(name)
                techGroup.write("%s"%gun_tech_list_ger[x])
                break
            x +=1
            if x == 27:
                break
        for name in hanger:
            if name in tech:
                techGroup.write(" %s"%hanger_tech_list_ger[y])
                break
            y +=1
            if y == 2:
                break
        for name in launcer:
            if name in tech:
                techGroup.write(" %s\""%launcher_tech_list_ger[z])
                break
            z +=1
            if z == 3:
                break
    techGroup.write("\n")
    for tech,module in tech_set.items():
        techGroup.write("\n %s_desc:0 \"\""%tech)
    techGroup.close()

def local_tech_cn(tech_set, file, gun, hanger, launcer):
    techGroup = open(file, "w", encoding='utf-8-sig')
    techGroup.write("l_english:\n")

    gun_tech_list_cn = ["基本枪组", "改良型115-135mm炮组", "先进型115-135mm炮组", "90-115mm两用炮组", "先进型 90-115mm两用炮组", "改良135-160mm炮组", "先进型135-160mm炮组", "145-160mm速射炮组", "135-145mm两用炮组", "先进型135-145mm两用炮组", "145-160mm两用炮组", "180-210mm炮组", "改良型180-210mm炮组", "先进型180-210mm炮组", "180-210mm速射炮组", "改良型250-310mm炮组", "先进型250-310mm炮组", "320-360mm炮组", "改良型320-360mm炮组", "先进型320-360mm炮组", "380-420mm炮组", "改良型380-420mm炮组", "先进型380-420mm炮组", "改良型450-480mm炮组", "先进型450-480mm炮组", "改良型500-520mm炮组", "先进型500-520mm炮组"]
    hanger_tech_list_cn = ["转换衣架", "装甲衣架"]
    launcher_tech_list_cn = ["小", "介质", "大"]
    
    for tech,module in tech_set.items():
        techGroup.write("\n %s:0 \""%tech)
        x=0
        y=0
        z=0
        for name in gun:
            if name in tech:
                #print(name)
                techGroup.write("%s"%gun_tech_list_cn[x])
                break
            x +=1
            if x == 27:
                break
        for name in hanger:
            if name in tech:
                techGroup.write("%s"%hanger_tech_list_cn[y])
                break
            y +=1
            if y == 2:
                break
        for name in launcer:
            if name in tech:
                techGroup.write("%s\""%launcher_tech_list_cn[z])
                break
            z +=1
            if z == 3:
                break
        
        #techGroup.write("%s\""%tech.replace("_", " "))
    techGroup.write("\n")
    for tech,module in tech_set.items():
        techGroup.write("\n %s:0 \"\""%tech)
    techGroup.close()

def local_tech_jp(tech_set, file, gun, hanger, launcer):
    techGroup = open(file, "w", encoding='utf-8-sig')
    techGroup.write("l_english:\n")

    gun_tech_list = ["基本バッテリー", "改良型 115-135mm砲", "発展型 115-135mm砲", "115-135mm両用砲", "発展型 115-135mm両用砲", "改良型 135-160mm砲", "発展型 135-160mm砲", "145-160mm速射砲", "135-145mm両用砲", "発展型 135-145mm両用砲", "145-160mm両用砲", "180-210mm砲", "改良型 180-210mm砲", "発展型 180-210mm砲", "180-210mm速射砲", "改良型 250-310mm砲", "発展型 250-310mm砲", "320-360mm砲", "改良型 320-360mm砲", "発展型 320-360mm砲", "380-420mm砲", "改良型 380-420mm砲", "発展型 380-420mm砲", "改良型 450-480mm砲", "発展型 450-480mm砲", "改良型 500-520mm砲", "発展型 500-520mm砲"]
    hanger_tech_list = ["改造ハンガー", "装甲ハンガー"]
    launcher_tech_list = ["小", "中", "大"]
    
    for tech,module in tech_set.items():
        techGroup.write("\n %s:0 \""%tech)
        x=0
        y=0
        z=0
        for name in gun:
            if name in tech:
                #print(name)
                techGroup.write("%s"%gun_tech_list_ger[x])
                break
            x +=1
            if x == 27:
                break
        for name in hanger:
            if name in tech:
                techGroup.write(" %s"%hanger_tech_list_ger[y])
                break
            y +=1
            if y == 2:
                break
        for name in launcer:
            if name in tech:
                techGroup.write(" %s\""%launcher_tech_list_ger[z])
                break
            z +=1
            if z == 3:
                break
    techGroup.write("\n")
    for tech,module in tech_set.items():
        techGroup.write("\n %s:0 \"\""%tech)
    techGroup.close()

#Top View for showing off moduels
def top_view_deck(file):
    topView = open(file, "a+", encoding='utf-8-sig')
    if "capital" in file:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"nrm_capital_flightdeck\"")
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"flight_deck\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_heavy_flight_deck_short\"")
        topView.write("\n\t\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"nrm_capital_flightdeck_long\"")
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"flight_deck\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_heavy_flight_deck_long\"")
        topView.write("\n\t\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")
    else:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"nrm_cruiser_flightdeck\"")
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"flight_deck\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_cruiser_flight_deck_short\"")
        topView.write("\n\t\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"nrm_cruiser_flightdeck_long\"")
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"flight_deck\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_cruiser_flight_deck_long\"")
        topView.write("\n\t\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    topView.write("\n\t\t\t}")

    topView.close()

def top_view_hybrid(module_set, file):
    completed_list = []
    #Magic position stuff
    captial_turret_gun_count= ["","","GFX_SM_nrm_capital_battery_twin_rear","GFX_SM_nrm_capital_battery_triple_rear","GFX_SM_nrm_capital_battery_quad_rear"]
    captial_turret_pos= ["","x=110 y=0","x=161 y=0","x=110 y=0","x=161 y=0"]
    cruiser_turret_gun_count= ["","","GFX_SM_nrm_cruiser_battery_twin_rear","GFX_SM_nrm_cruiser_battery_triple_rear","GFX_SM_nrm_cruiser_battery_twin","GFX_SM_nrm_cruiser_battery_triple"]
    cruiser_turret_pos= ["x=160 y=0","x=155 y=0","x=200 y=0","x=190 y=0"]
    PB_turret_pos= ["","x=175 y=2","x=338 y=2"]

    topView = open(file, "a+", encoding='utf-8-sig')
    print()
    print()
    print("--           Sarting Top View            --")
    print()
    for module in module_set:
        if module.add_carrier_size > 0:
            if "capital" in module.name:
                #print(module.category[-2:])
                if "_long" in module.category2:
                    #tmp_catagory = module.gui_category + "_long"
                    tmp_catagory = module.category + "_long"
                else:
                    #tmp_catagory = module.gui_category
                    tmp_catagory = module.category
                if not (tmp_catagory in completed_list):
                    completed_list.append(tmp_catagory)

                    topView.write("\n\t\t\t\tcontainerWindowType = {")
                    if not "_long" in tmp_catagory:
                        #topView.write("\n\t\t\t\t\tname = \"%s\""%module.gui_category)
                        topView.write("\n\t\t\t\t\tname = \"%s\""%module.category)
                    else:
                        #topView.write("\n\t\t\t\t\tname = \"%s_long\""%module.gui_category)
                        topView.write("\n\t\t\t\t\tname = \"%s_long\""%module.category)
                    topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
                    topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")

                    #flight deck
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"flight_deck\"")
                    if not "_long" in tmp_catagory:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_heavy_flight_deck_short\"")
                    else:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_heavy_flight_deck_long\"")
                    topView.write("\n\t\t\t\t\t\tposition = { x=0 y=0 }")
                    topView.write("\n\t\t\t\t\t}")

                    #Guns
                    tmp_turret = module.category.split("x")
                    guns_per_turret = int(tmp_turret[0][-1:])
                    turrets = int(tmp_turret[1][:1])
                    turret_counter = 1
                    while turret_counter <= turrets:
                        topView.write("\n\t\t\t\t\ticonType = {")
                        topView.write("\n\t\t\t\t\t\tname = \"image%i\""%turret_counter)
                        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count[guns_per_turret])
                        topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos[turret_counter])
                        topView.write("\n\t\t\t\t\t}")
                        turret_counter = turret_counter +1
                    topView.write("\n\t\t\t\t}\n")
            i=0
            if "cruiser" in module.name:
                if "_long" in module.category2:
                    #if module.caliber <5.9:
                    #    tmp_catagory = module.gui_category[:-3] + "L_" + module.gui_category[-3:] + "_long"
                    #elif module.caliber >5.9 and module.caliber <8.1:
                    #    tmp_catagory = module.gui_category[:-3] + "H_" + module.gui_category[-3:] + "_long"
                    #else:
                    #    tmp_catagory = module.gui_category + "_long"
                    tmp_catagory = module.category + "_long"
                else:
                    #if module.caliber <5.9:
                    #    tmp_catagory = module.gui_category[:-3] + "L_" + module.gui_category[-3:]
                    #elif module.caliber >5.9 and module.caliber <8.1:
                    #    tmp_catagory = module.gui_category[:-3] + "H_" + module.gui_category[-3:]
                    #else:
                    #    tmp_catagory = module.gui_category
                    tmp_catagory = module.category
                if not (tmp_catagory in completed_list):
                    completed_list.append(tmp_catagory)

                    topView.write("\n\t\t\t\tcontainerWindowType = {")
                    topView.write("\n\t\t\t\t\tname = \"%s\""%tmp_catagory)
                    topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
                    topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")

                    #flight deck
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"flight_deck\"")
                    if not "_long" in tmp_catagory:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_cruiser_flight_deck_short\"")
                    else:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_cruiser_flight_deck_long\"")
                    topView.write("\n\t\t\t\t\t\tposition = { x=0 y=0 }")
                    topView.write("\n\t\t\t\t\t}")

                    #cruiser guns
                    if "_x0" in tmp_catagory:
                        tmp_turret = module.category.split("x")
                        num_guns = int(tmp_turret[1][:2])
                        if num_guns%3 == 0:
                            gun_counter = 3
                            while gun_counter <= num_guns:
                                topView.write("\n\t\t\t\t\ticonType = {")
                                topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(gun_counter/3))
                                if module.caliber >5.9 and module.caliber <8.1:
                                    topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple")
                                else:
                                    topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_light")
                                if gun_counter >3:
                                    topView.write("\"")
                                else:
                                    topView.write("_rear\"")
                                topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos[1])
                                topView.write("\n\t\t\t\t\t}")
                                gun_counter = gun_counter +3
                        elif num_guns%2 ==0:
                            gun_counter = 2
                            while gun_counter <= num_guns:
                                topView.write("\n\t\t\t\t\ticonType = {")
                                topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(gun_counter/2))
                                if module.caliber >5.9 and module.caliber <8.1:
                                    topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin")
                                else:
                                    topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light")
                                if gun_counter >2:
                                    topView.write("\"")
                                else:
                                    topView.write("_rear\"")
                                topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos[1])
                                topView.write("\n\t\t\t\t\t}")
                                gun_counter = gun_counter +2
                
                    #PB guns
                    elif "_PB_" in tmp_catagory:
                        tmp_turret = module.category.split("x")
                        guns_per_turret = int(tmp_turret[0][-1:])
                        turrets = int(tmp_turret[1][:1])
                        turret_counter = 1
                        while turret_counter <= turrets:
                            topView.write("\n\t\t\t\t\ticonType = {")
                            topView.write("\n\t\t\t\t\t\tname = \"image%i\""%turret_counter)
                            if turret_counter >2:
                                topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_capital_battery_twin_rear\"")
                            else:
                                topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count[guns_per_turret])
                            #print(turret_counter)
                            #print(PB_turret_pos[turret_counter])
                            topView.write("\n\t\t\t\t\t\tposition = { %s }"%PB_turret_pos[1])
                            topView.write("\n\t\t\t\t\t}")
                            turret_counter = turret_counter +1
                    topView.write("\n\t\t\t\t}")

        #print(completed_list)
    #topView.write("\n\t\t\t}")
    topView.close()
    top_view_deck(file)

    if "capital" in file:
        Modues_gui = open("Output\_module lists\_Capital Modules Category.txt","w")
        for module in completed_list:
            Modues_gui.write("\n%s"%module)
    else:
        Modues_gui = open("Output\_module lists\_Cruiser Modules Category.txt","w")
        for module in completed_list:
            Modues_gui.write("\n%s"%module)
    Modues_gui.close()

i=0
def top_view_guns(module_set, module_set_rear, file, hybrid_set):
    #Magic position stuff
    captial_turret_gun_count_front= ["","","GFX_SM_nrm_capital_battery_twin","GFX_SM_nrm_capital_battery_triple","GFX_SM_nrm_capital_battery_quad"]
    captial_turret_pos_front= ["x=395 y=0","x=365 y=0","x=332 y=0","x=110 y=0","x=161 y=0"]
    captial_turret_gun_count_rear= ["","","GFX_SM_nrm_capital_battery_twin_rear","GFX_SM_nrm_capital_battery_triple_rear","GFX_SM_nrm_capital_battery_quad_rear"]
    captial_turret_pos_rear= ["","x=77 y=0","x=110 y=0","x=194 y=0","x=161 y=0"]

    cruiser_turret_gun_count_front= ["","","GFX_SM_nrm_cruiser_battery_twin","GFX_SM_nrm_cruiser_battery_triple"]
    #cruiser_turret_pos_front= ["","x=388 y=0","x=356 y=0","x=334 y=0"]
    cruiser_turret_pos_front= ["","x=388 y=0","x=356 y=0","x=334 y=0","x=380 y=0","x=365 y=0","x=335 y=0","x=352 y=0","x=374 y=0"]
    PB_turret_pos_front= ["x=345 y=2","x=366 y=2","x=338 y=2"]
    cruiser_turret_gun_count_rear= ["","","GFX_SM_nrm_cruiser_battery_twin_rear","GFX_SM_nrm_cruiser_battery_triple_rear"]
    cruiser_turret_pos_rear= ["x=90 y=0","x=102 y=0","x=132 y=0","x=140 y=0","x=160 y=0","x=170 y=0"]
    PB_turret_pos_rear= ["x=100 y=3","x=87 y=3","x=115 y=3"]

    topView = open(file, "w", encoding='utf-8-sig')
    #front battery modules
    topView.write("\t\t\t################# MODULE SLOT: Heavy Battery #################")
    topView.write("\n\t\t\tcontainerWindowType = {\n\t\t\t\tname = \"fixed_ship_battery_slot\"\n\t\t\t\tposition = { x=0 y=0 }\n\t\t\t\tsize = { width=100% height=100% }\n")
    for module in module_set:
        #print(module.category)
        if "capital" in module.category:
            topView.write("\n\t\t\t\tcontainerWindowType = {")
            topView.write("\n\t\t\t\t\tname = \"%s\""%module.category)
            topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
            topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }\n")
        
            tmpTurretCount = 1
            #print(module.numberTurrets)
            while tmpTurretCount <= module.numberTurrets:
                topView.write("\n\t\t\t\t\ticonType = {")
                topView.write("\n\t\t\t\t\t\tname = \"image%i\""%tmpTurretCount)
                if "4x1_2x1" in module.category or "3x1_2x1" in module.category: #spacific case with mixed gun per terret layout
                    if "4x1" in module.category:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[4])
                    elif "3x1" in module.category:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[3])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_front[tmpTurretCount])
                    tmpTurretCount += 1
                    topView.write("\n\t\t\t\t\t}")
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%tmpTurretCount)
                    topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[2])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_front[tmpTurretCount])
                elif module.numberTurrets == 1: #put single turrets on barbet
                    topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[int(module.numberGuns / module.numberTurrets)])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_front[2])
                elif module.numberTurrets == 3: #Nelson style layout
                    if tmpTurretCount==1: 
                        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[int(module.numberGuns / module.numberTurrets)])
                        topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_front[0])
                    elif tmpTurretCount==2: 
                        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[int(module.numberGuns / module.numberTurrets)])
                        topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_front[2])
                    else:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[int(module.numberGuns / module.numberTurrets)])
                        topView.write("\n\t\t\t\t\t\tposition = { x=368 y=0 }")
                else: #normal layouts
                    topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[int(module.numberGuns / module.numberTurrets)])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_front[tmpTurretCount])
                topView.write("\n\t\t\t\t\t}")
                tmpTurretCount += 1
            topView.write("\n\t\t\t\t}")
        if "cruiser" in module.category:
            topView.write("\n\t\t\t\tcontainerWindowType = {")
            topView.write("\n\t\t\t\t\tname = \"%s\""%module.category)
            topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
            topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }\n")

            if "_x0" in module.category:
                tmp_turret = module.category.split("x")
                num_guns = int(tmp_turret[1][:2])
                if num_guns == 5: #Pensacola 
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(1))
                    if module.caliber >5.9 and module.caliber <8.2:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin\"")
                    else:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(5)])
                    topView.write("\n\t\t\t\t\t}")

                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(2))
                    if module.caliber >5.9 and module.caliber <8.2:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple\"")
                    else:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_light\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(6)])
                    topView.write("\n\t\t\t\t\t}")
                elif num_guns == 9 or (num_guns == 6 and module.caliber > 7.9): #Brooklyn and Jap Heavy cruisers
                    #front
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(1))
                    if num_guns == 9:
                        if module.caliber >5.9 and module.caliber <8.1:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_light\"")
                    else:
                        if module.caliber >5.9 and module.caliber <8.2:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(4)])
                    topView.write("\n\t\t\t\t\t}")
                    #back
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(2))
                    if num_guns == 9:
                        if module.caliber >5.9 and module.caliber <8.1:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_rear\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_light_rear\"")
                    else:
                        if module.caliber >5.9 and module.caliber <8.1:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_rear\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light_rear\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(6)])
                    topView.write("\n\t\t\t\t\t}")
                    #mid
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(3))
                    if num_guns == 9:
                        if module.caliber >5.9 and module.caliber <8.1:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_light\"")
                    else:
                        if module.caliber >5.9 and module.caliber <8.1:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(5)])
                    topView.write("\n\t\t\t\t\t}")
                elif num_guns == 6 and module.caliber < 5.9: #Atlanta, Juneau, Dido
                    #front
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(1))
                    topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(8)])
                    topView.write("\n\t\t\t\t\t}")
                    #mid
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(2))
                    topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(7)])
                    topView.write("\n\t\t\t\t\t}")
                    #rear
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(3))
                    topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(3)])
                    topView.write("\n\t\t\t\t\t}")
                elif num_guns%3 == 0:
                    gun_counter = 3
                    while gun_counter <= num_guns:
                        topView.write("\n\t\t\t\t\ticonType = {")
                        topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(gun_counter/3))
                        if module.caliber >5.9 and module.caliber <8.2:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_light\"")
                        if gun_counter == 3 and not module.numberGuns == 3:
                            topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(5)])
                        else:
                            topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(6)])
                        topView.write("\n\t\t\t\t\t}")
                        gun_counter = gun_counter +3
                elif num_guns%2 ==0:
                    gun_counter = 2
                    while gun_counter <= num_guns:
                        topView.write("\n\t\t\t\t\ticonType = {")
                        topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(gun_counter/2))
                        if module.caliber >5.9 and module.caliber <8.2:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light\"")
                        if gun_counter == 2 and not module.numberGuns == 2:
                            topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(5)])
                        else:
                            topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_front[int(6)])
                        topView.write("\n\t\t\t\t\t}")
                        gun_counter = gun_counter +2

            #PB guns
            elif "_PB_" in module.category:
                tmp_turret = module.category.split("x")
                guns_per_turret = int(tmp_turret[0][-1:])
                turrets = int(tmp_turret[1][:1])
                turret_counter = 1
                while turret_counter <= turrets:
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%turret_counter)
                    topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_front[guns_per_turret])
                    #print(turret_counter)
                    #print(PB_turret_pos[turret_counter])
                    if module.numberTurrets == 1:
                        topView.write("\n\t\t\t\t\t\tposition = { %s }"%PB_turret_pos_front[0])
                    else:
                        topView.write("\n\t\t\t\t\t\tposition = { %s }"%PB_turret_pos_front[turret_counter])
                    topView.write("\n\t\t\t\t\t}")
                    turret_counter = turret_counter +1
            topView.write("\n\t\t\t\t}")

    topView.write("\n\t\t\t}")
    

    #rear battery modules
    topView.write("\n\n\t\t\t################# MODULE SLOT: Heavy Battery Rear #################")
    topView.write("\n\t\t\tcontainerWindowType = {\n\t\t\t\tname = \"fixed_ship_battery_rear_slot\"\n\t\t\t\tposition = { x=0 y=0 }\n\t\t\t\tsize = { width=100% height=100% }\n")
    for module in module_set_rear:
        #print(module.category)
        if "capital" in module.category:
            topView.write("\n\t\t\t\tcontainerWindowType = {")
            topView.write("\n\t\t\t\t\tname = \"%s\""%module.category)
            topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
            topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }\n")
        
            tmpTurretCount = 1
            #print(module.numberTurrets)
            while tmpTurretCount <= module.numberTurrets:
                topView.write("\n\t\t\t\t\ticonType = {")
                topView.write("\n\t\t\t\t\t\tname = \"image%i\""%tmpTurretCount)
                if "4x1_2x1" in module.category or "3x1_2x1" in module.category: #spacific case with mixed gun per terret layout
                    if "4x1" in module.category:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_rear[4])
                    elif "3x1" in module.category:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_rear[3])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_rear[tmpTurretCount])
                    tmpTurretCount += 1
                    topView.write("\n\t\t\t\t\t}")
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%tmpTurretCount)
                    topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_rear[2])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_rear[tmpTurretCount])
                elif module.numberTurrets == 1: #put single turrets on barbet
                    topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_rear[int(module.numberGuns / module.numberTurrets)])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_rear[2])
                else: #normal layouts
                    topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_rear[int(module.numberGuns / module.numberTurrets)])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%captial_turret_pos_rear[tmpTurretCount])
                topView.write("\n\t\t\t\t\t}")
                tmpTurretCount += 1
            topView.write("\n\t\t\t\t}")
        if "cruiser" in module.category:
            topView.write("\n\t\t\t\tcontainerWindowType = {")
            topView.write("\n\t\t\t\t\tname = \"%s\""%module.category)
            topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
            topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }\n")
            if "_x0" in module.category:
                tmp_turret = module.category.split("x")
                num_guns = int(tmp_turret[1][:2])
                if num_guns == 5: #Pensacola 
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(1))
                    if module.caliber >5.9 and module.caliber <8.2:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_rear\"")
                    else:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light_rear\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_rear[int(1)])
                    topView.write("\n\t\t\t\t\t}")

                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(2))
                    if module.caliber >5.9 and module.caliber <8.2:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_rear\"")
                    else:
                        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_light_rear\"")
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_rear[int(2)])
                    topView.write("\n\t\t\t\t\t}")
                if num_guns%3 == 0:
                    gun_counter = 3
                    while gun_counter <= num_guns:
                        topView.write("\n\t\t\t\t\ticonType = {")
                        topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(gun_counter/3))
                        if module.caliber >5.9 and module.caliber <8.1:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_rear\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_triple_light_rear\"")
                        topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_rear[int(gun_counter/3)])
                        topView.write("\n\t\t\t\t\t}")
                        gun_counter = gun_counter +3
                elif num_guns%2 ==0:
                    gun_counter = 2
                    while gun_counter <= num_guns:
                        topView.write("\n\t\t\t\t\ticonType = {")
                        topView.write("\n\t\t\t\t\t\tname = \"image%i\""%(gun_counter/2))
                        if module.caliber >5.9 and module.caliber <8.1:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_rear\"")
                        else:
                            topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_cruiser_battery_twin_light_rear\"")
                        topView.write("\n\t\t\t\t\t\tposition = { %s }"%cruiser_turret_pos_rear[int(gun_counter/2)])
                        topView.write("\n\t\t\t\t\t}")
                        gun_counter = gun_counter +2

            #PB guns
            elif "_PB_" in module.category:
                tmp_turret = module.category.split("x")
                guns_per_turret = int(tmp_turret[0][-1:])
                turrets = int(tmp_turret[1][:1])
                turret_counter = 1
                while turret_counter <= turrets:
                    topView.write("\n\t\t\t\t\ticonType = {")
                    topView.write("\n\t\t\t\t\t\tname = \"image%i\""%turret_counter)
                    topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%captial_turret_gun_count_rear[guns_per_turret])
                    #print(turret_counter)
                    #print(PB_turret_pos[turret_counter])
                    topView.write("\n\t\t\t\t\t\tposition = { %s }"%PB_turret_pos_rear[turret_counter])
                    topView.write("\n\t\t\t\t\t}")
                    turret_counter = turret_counter +1
            topView.write("\n\t\t\t\t}")
    i=0
    topView.close()
    top_view_hybrid(hybrid_set, file)

def top_view_subs(module_set_forward, module_set_aft, module_set_fantail, file):
    #Magic Position Stuff
    sub_turret_size_front   = ["GFX_SM_RP_submarine_light_battery_F","GFX_SM_RP_submarine_light_battery_FS","GFX_SM_RP_submarine_medium_battery_F","GFX_SM_LF_submarine_heavy_battery_F"] 
    sub_turret_pos_front    = ["x=284 y=-9","x=253 y=-17","x=224 y=-20","x=0 y=0"] 
    sub_turret_size_rear    = ["GFX_SM_RP_submarine_light_battery_R","GFX_SM_RP_submarine_light_battery_RS","GFX_SM_RP_submarine_medium_battery_R"] 
    sub_turret_pos_rear     = ["x=155 y=-9","x=186 y=-3","x=148 y=-20","x=204 y=-20","x=100 y=-8"] 

    sub_deckgun_size_front  = ["GFX_SM_RP_submarine_deckgun_F","GFX_SM_RP_submarine_deckgun_FS"] 
    sub_deckgun_pos_front   = ["x=284 y=-10","x=253 y=-17"] 
    sub_deckgun_size_rear   = ["GFX_SM_RP_deckgun_R","GFX_SM_RP_deckgun_RS"] 
    sub_deckgun_pos_rear    = ["x=153 y=-11","x=186 y=-3","x=103 y=-11"] 

    sub_hanger_size_front   = ["GFX_SM_RP_submarine_hanger_1_F"] 
    sub_hanger_pos_front    = ["x=161 y=-18"]
    sub_hanger_size_rear    = ["GFX_SM_RP_submarine_hanger_1_R","GFX_SM_RP_submarine_hanger_2_R"] 
    sub_hanger_pos_rear     = ["x=161 y=-24","x=161 y=-18"] 

    sub_aa_size_front       = ["GFX_SM_RP_submarine_anti_air_F"] 
    sub_aa_pos_front        = ["x=251 y=-17"] 
    sub_aa_size_rear        = ["GFX_SM_RP_submarine_anti_air_R","GFX_SM_RP_submarine_anti_air_RS"] 
    sub_aa_pos_rear         = ["x=186 y=-3","x=200 y=-8"] 

    topView = open(file, "w", encoding='utf-8-sig')

    
    ##- Forward Conning Tower -##
    topView.write("\n\t\t\t################# MODULE SLOT: Forward Conning Tower (Fixed Battery) #################")
    topView.write("\n\t\t\tcontainerWindowType = {\n\t\t\t\tname = \"fixed_ship_battery_slot\"\n\t\t\t\tposition = { x=0 y=0 }\n\t\t\t\tsize = { width=100% height=100% }\n")
    
    #AA
    AAList = ["nrm_submarine_AA","nrm_submarine_HAA"]
    topView.write("\n\t\t\t\t#### MODULE: Anti Air ####")
    for cat in AAList:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%cat)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_aa_size_front[0])
        topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_aa_pos_front[0])
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    #Hangers
    HangerList = ["nrm_submarine_FP","nrm_submarine_cvl"]
    topView.write("\n\t\t\t\t#### MODULE: Hangers ####")
    for cat in HangerList:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%cat)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_hanger_size_front[0])
        topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_hanger_pos_front[0])
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    #Turrets/Deckguns
    topView.write("\n\t\t\t\t#### MODULE: Guns ####")
    for module in module_set_forward:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%module.category)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        if "deckgun" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_deckgun_size_front[0])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_deckgun_pos_front[0])
        elif "heavy" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_turret_size_front[3])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_turret_pos_front[3])
        elif "medium" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_turret_size_front[2])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_turret_pos_front[2])
        elif "light" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_turret_size_front[0])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_turret_pos_front[0])
        topView.write("\n\t\t\t\t\t}")
        if module.numberGuns>3 or "_x2" in module.category:
            topView.write("\n\t\t\t\t\ticonType = {")
            topView.write("\n\t\t\t\t\t\tname = \"image2\"")
            if module.numberGuns>3:
                topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_turret_size_front[1])
                topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_turret_pos_front[1])
            elif "deckgun" in module.name:
                topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_deckgun_size_front[1])
                topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_deckgun_pos_front[1])
            topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")
    topView.write("\n\t\t}") 



    ##- Rear Conning Tower -##
    topView.write("\n\t\t\t################# MODULE SLOT: Rear Conning Tower (Custom 2) #################")
    topView.write("\n\t\t\tcontainerWindowType = {\n\t\t\t\tname = \"custom_slot_2\"\n\t\t\t\tposition = { x=0 y=0 }\n\t\t\t\tsize = { width=100% height=100% }\n")
    
    #Blanks
    BlankList = ["nrm_submarine_SNK","nrm_submarine_ML"]
    topView.write("\n\t\t\t\t#### MODULE: Blanks ####")
    for cat in BlankList:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%cat)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_blank\"")
        topView.write("\n\t\t\t\t\t\tposition = { x=100 y=0 }")
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    #AA
    AAList = ["nrm_submarine_AA","nrm_submarine_HAA"]
    topView.write("\n\t\t\t\t#### MODULE: Anti Air ####")
    for cat in AAList:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%cat)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_aa_size_rear[0])
        topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_aa_pos_rear[0])
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    #Hangers
    HangerList = ["nrm_submarine_FP","nrm_submarine_cvl","nrm_submarine_cv"]
    topView.write("\n\t\t\t\t#### MODULE: Hangers ####")
    for cat in HangerList:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%cat)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        if cat == "nrm_submarine_cv":
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_hanger_size_rear[1])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_hanger_pos_rear[1])
        else:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_hanger_size_rear[0])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_hanger_pos_rear[0])
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    #Turrets/Deckguns
    topView.write("\n\t\t\t\t#### MODULE: Guns ####")
    for module in module_set_aft:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%module.category)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        if "deckgun" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_deckgun_size_rear[0])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_deckgun_pos_rear[0])
        elif "medium" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_turret_size_rear[2])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_turret_pos_rear[2])
        elif "light" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_turret_size_rear[0])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_turret_pos_rear[0])
        topView.write("\n\t\t\t\t\t}")
        if module.numberGuns>3 or "_x2" in module.category:
            topView.write("\n\t\t\t\t\ticonType = {")
            topView.write("\n\t\t\t\t\t\tname = \"image2\"")
            if module.numberGuns>3:
                topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_turret_size_rear[1])
                topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_turret_pos_rear[1])
            elif "deckgun" in module.name:
                topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_deckgun_size_rear[1])
                topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_deckgun_pos_rear[1])
            topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")
    topView.write("\n\t\t}")



    ##- Fan Tail -##
    topView.write("\n\t\t\t################# MODULE SLOT: Fan Tail (Custom 3) #################")
    topView.write("\n\t\t\tcontainerWindowType = {\n\t\t\t\tname = \"custom_slot_3\"\n\t\t\t\tposition = { x=0 y=0 }\n\t\t\t\tsize = { width=100% height=100% }\n")
    
    #Blanks
    topView.write("\n\t\t\t\t#### MODULE: Blanks ####")
    BlankList = ["nrm_submarine_SNK","nrm_submarine_ML"]
    for cat in BlankList:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%cat)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_blank\"")
        topView.write("\n\t\t\t\t\t\tposition = { x=100 y=0 }")
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    #Turrets/Deckguns
    topView.write("\n\t\t\t\t#### MODULE: Guns ####")
    for module in module_set_fantail:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%module.category)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        if "deckgun" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_deckgun_size_rear[0])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_deckgun_pos_rear[2])
        elif "light" in module.gui_category:
            topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_turret_size_rear[0])
            topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_turret_pos_rear[4])
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")
    topView.write("\n\t\t}")



    ##- Anti Air -##
    topView.write("\n\t\t\t################# MODULE SLOT: Anti Air #################")
    topView.write("\n\t\t\tcontainerWindowType = {\n\t\t\t\tname = \"fixed_ship_anti_air_slot\"\n\t\t\t\tposition = { x=0 y=0 }\n\t\t\t\tsize = { width=100% height=100% }\n")
    
    #AA
    topView.write("\n\t\t\t\t#### MODULE: Anti Air ####")
    AAList = ["nrm_submarine_AA","nrm_submarine_HAA"]
    for cat in AAList:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%cat)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"%s\""%sub_aa_size_rear[1])
        topView.write("\n\t\t\t\t\t\tposition = { %s }"%sub_aa_pos_rear[1])
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    topView.write("\n\t\t}")



    ##- Custom 1 -##
    topView.write("\n\t\t\t################# MODULE SLOT: Custom 1 #################")
    topView.write("\n\t\t\tcontainerWindowType = {\n\t\t\t\tname = \"custom_slot_1\"\n\t\t\t\tposition = { x=0 y=0 }\n\t\t\t\tsize = { width=100% height=100% }\n")
    
    #Blanks
    topView.write("\n\t\t\t\t#### MODULE: Blanks ####")
    BlankList = ["nrm_submarine_SNK","nrm_submarine_ML"]
    for cat in BlankList:
        topView.write("\n\t\t\t\tcontainerWindowType = {")
        topView.write("\n\t\t\t\t\tname = \"%s\""%cat)
        topView.write("\n\t\t\t\t\tposition = { x=0 y=0 }")
        topView.write("\n\t\t\t\t\tsize = { width=100% height=100% }")
        topView.write("\n\t\t\t\t\ticonType = {")
        topView.write("\n\t\t\t\t\t\tname = \"image\"")
        topView.write("\n\t\t\t\t\t\tspriteType = \"GFX_SM_nrm_blank\"")
        topView.write("\n\t\t\t\t\t\tposition = { x=100 y=0 }")
        topView.write("\n\t\t\t\t\t}")
        topView.write("\n\t\t\t\t}")

    topView.write("\n\t\t}")


    topView.close()
i=0
valid_capital_gun_batteries = ["_2x2 ", "_2x3 ", "_2x4 ", "_3x1 ", "_3x2 ", "_4x1 ", "_4x2", "_3x1_2x1 ", "_4x1_2x1 "]
valid_capital_gun_batteries2 = ["_2x1", "_2x2 ", "_3x1 ", "_4x1 "]
exceptions_capital_gun_batteries = ["a3x2", "a4x2"]
valid_cruiser_gun_batteries = ["_2x1 ", "_2x2 ", "_3x1 ", "_3x2 ", "_4x1 " , "_4x2 ", "_x02", "_x03", "_x04", "_x06", "_x08" ,"_x09"]
valid_cruiser_gun_batteries2 = ["_2x1 ", "_x02", "_x03", "_x04", "_x06"]
exceptions_cruiser_gun_batteries = []
#valid_carrier_flight_deck = ["CHL_010", "CHL_015", "CHL_020", "CHL_025", "CHL_030", "AHL_010", "AHL_015", "AHL_020", "AHL_025", "AHL_030"]
valid_carrier_flight_deck = ["CHL_010", "CHL_020", "CHL_030"]

valid_module = False
exception_gun = False
stat_sub_catagory = ""
capital_gun_batteries_array = []
capital_gun_batteries_array_singles = []
cruiser_gun_batteries_array = []
cruiser_gun_batteries_array_temp = []
carrier_flight_deck_array = []
tmp_carrier_flight_deck_array = []
capital_hybrid_array = []
cruiser_hybrid_array = []
submarine_deck_gun_array = []

tech_array = []
tech_hybrid_array = []

surface_gun_list = []

#capital_gun_batteries = [] #= open("input\\modules\\nrm_capital_battery.txt", "r+")
#cruiser_gun_batteries = [] #= open("input\\modules\\nrm_cruiser_battery.txt", "r+")
#carrier_flight_deck = [] #= open("input\\modules\\nrm_carrier_flightdeck.txt", "r+")


#Grab Module data from input\modules
def GetModuleData():
    moduleFiles = glob.glob("input/modules/*.txt")
    if BICE:
        moduleFiles = glob.glob("input/modules/BICE/*.txt")
    capital_gun_batteries_array.clear()
    cruiser_gun_batteries_array.clear()
    carrier_flight_deck_array.clear()
    submarine_deck_gun_array.clear()
    for moduleFile in moduleFiles:
        indintation = 0
        file = open(moduleFile)
        module = DefModule()

        newModule = False
        capitalShipGun = False
        cruiserShipGun = False
        flightDeck = False
        submarineDeckGun = False

        add_stats_section = False
        add_average_stats_section = False
        multiply_stats_section = False
        build_cost_resources_section = False
        for line in file:
            try:
                if indintation == 1:
                    if "nrm_capital_battery" in line:
                        for m in valid_capital_gun_batteries:
                            if m in line:
                                newModule = True
                                break
                        for m in exceptions_capital_gun_batteries:
                            if m in line:
                                newModule = False
                                #print(line)
                                break
                        for m in capital_gun_batteries_array:
                            if line.split("=")[0].strip() == m.name:
                                newModule = False
                                break
                        if newModule:
                            capitalShipGun = True
                            #print(line.split("=")[0].strip())
                            module = DefModule()
                            module.name = line.split("=")[0].strip()
                            module.caliber = int(module.name.split("battery_")[1].split("_")[0])
                            module.level = int(line[line.find("battery_")+11])
                            module.numberTurrets = int(line[line.find("x")+1])
                            module.numberGuns = module.numberTurrets * int(line[line.find("x")-1])
                            if "_DP_" in module.name:
                                dualPurpse = True
                        pass
                    elif "nrm_cruiser_battery" in line:
                        for m in valid_cruiser_gun_batteries:
                            if m in line:
                                newModule = True
                                break
                        for m in exceptions_capital_gun_batteries:
                            if m in line:
                                newModule = False
                                print(line)
                                break
                        for m in capital_gun_batteries_array:
                            if line.split("=")[0].strip() == m.name:
                                newModule = False
                                break
                        if newModule:
                            cruiserShipGun = True
                            module = DefModule()
                            module.name = line.split("=")[0].strip()
                            if "PB" in module.name:
                                module.caliber = int(module.name.split("PB_")[1].split("_")[0])
                                module.numberTurrets = int(line[line.find("x")+1])
                                module.numberGuns = module.numberTurrets * int(line[line.find("x")-1])
                            elif "5h" in module.name:
                                module.caliber = 5.5
                                module.numberGuns = int(module.name.split("_x")[1])
                            elif "_DP_" in module.name:
                                module.caliber = int(module.name.split("_DP_")[1].split("_")[0])
                                module.numberGuns = int(module.name.split("_x")[1])
                            else:
                                module.caliber = int(module.name.split("battery_")[1].split("_")[0])
                                module.numberGuns = int(module.name.split("_x")[1])
                            #print(module.name)
                            #print("\t%s"%module.name.split("_x")[1])
                            if "_DP_" in line:
                                module.dualPurpse = True
                                module.level = int(line[line.find("_x")-1])
                                #print("\t%s : DP"%module.name)
                                
                            elif "_PB_" in line:
                                module.level = int(line[line.find("_PB_")+7])
                            else:
                                module.level = int(line[line.find("_x")-1])
                    elif "nrm_carrier_flightdeck" in line:
                        for m in valid_carrier_flight_deck:
                            if m in line:
                                newModule = True
                                break
                        for m in capital_gun_batteries_array:
                            if line.split("=")[0].strip() == m.name:
                                newModule = False
                                break
                        if newModule:
                            flightDeck = True
                            module = DefModule()
                            module.name = line.split("=")[0].strip()
                            #print(module.name)
                    elif "nrm_submarine_deckgun" in line:
                        newModule = True
                        for m in capital_gun_batteries_array:
                            if line.split("=")[0].strip() == m.name:
                                newModule = False
                                break
                        if newModule:
                            submarineDeckGun = True
                            module = DefModule()
                            module.name = line.split("=")[0].strip()
                            #print(module.name)
                            module.caliber = int(module.name.split("deckgun_")[1].split("_")[0])
                            module.numberGuns = 1
                            #print(module.caliber)

                if indintation == 2:
                    if newModule:
                        if line.strip().startswith("category"):
                            #print(line.split("=")[1].strip())
                            module.category = line.split("=")[1].strip()
                        elif line.strip().startswith("gui_category"):
                            module.gui_category = line.split("=")[1].strip()
                        elif line.strip().startswith("parent"):
                            module.parent = line.split("=")[1].strip()
                        elif line.strip().startswith("add_equipment_type"):
                            module.add_equipment_type = line.split("=")[1].strip()
                        elif line.strip().startswith("manpower"):
                            module.manpower = int(line.split("=")[1].strip())
                        elif line.strip().startswith("add_stats"):
                            add_stats_section = True
                        elif line.strip().startswith("add_average_stats"):
                            add_average_stats_section = True
                        elif line.strip().startswith("multiply_stats"):
                            multiply_stats_section = True
                        elif line.strip().startswith("build_cost_resources"):
                            build_cost_resources_section = True
                        elif line.strip().startswith("critical_parts"):
                            #print(line.split("=")[1].replace("{","").replace("}","").strip())
                            module.critical_parts = line.split("=")[1].replace("{","").replace("}","").strip()
                        elif line.strip().startswith("dismantle_cost_ic"):
                            module.dismantle_cost_ic = float(line.split("=")[1].strip())
                if indintation == 3:
                    if newModule:
                        if add_stats_section:
                            if line.strip().startswith("build_cost_ic"):
                                module.add_build_cost_ic = float(line.split("=")[1].strip())
                                if module.numberTurrets > 0:
                                    module.ic_one_turret = float(module.add_build_cost_ic/module.numberTurrets)
                                if module.numberGuns > 0:
                                    module.ic_one_gun = float(module.add_build_cost_ic)/float(module.numberGuns)
                            elif line.strip().startswith("max_strength"):
                                module.add_max_strength = float(line.split("=")[1].strip())
                            elif line.strip().startswith("hg_attack"):
                                module.add_hg_attack = float(line.split("=")[1].strip())
                            elif line.strip().startswith("lg_attack"):
                                module.add_lg_attack = float(line.split("=")[1].strip())
                            elif line.strip().startswith("anti_air_attack"):
                                module.add_anti_air_attack = float(line.split("=")[1].strip())
                            elif line.strip().startswith("supply_consumption"):
                                module.add_supply_consumption = float(line.split("=")[1].strip())
                            elif line.strip().startswith("surface_visibility"):
                                module.add_surface_visibility = float(line.split("=")[1].strip())
                            elif line.strip().startswith("carrier_size"):
                                module.add_carrier_size = float(line.split("=")[1].strip())
                            elif line.strip().startswith("add_sub_visibility"):
                                module.add_sub_visibility = float(line.split("=")[1].strip())
                            elif line.strip().startswith("fuel_consumption"):
                                module.add_fuel_consumption = float(line.split("=")[1].strip())
                        if add_average_stats_section:
                            if line.strip().startswith("hg_armor_piercing"):
                                module.av_hg_armor_piercing = float(line.split("=")[1].strip())
                            elif line.strip().startswith("lg_armor_piercing"):
                                module.av_lg_armor_piercing = float(line.split("=")[1].strip())
                        if multiply_stats_section:
                            if line.strip().startswith("build_cost_ic"):
                                module.mp_build_cost_ic = float(line.split("=")[1].strip())
                            elif line.strip().startswith("reliability"):
                                module.mp_reliability = float(line.split("=")[1].strip())
                            elif line.strip().startswith("naval_speed"):
                                module.mp_naval_speed = float(line.split("=")[1].strip())
                            elif line.strip().startswith("fuel_consumption"):
                                module.mp_fuel_consumption = float(line.split("=")[1].strip())
                            elif line.strip().startswith("max_strength"):
                                module.mp_armor_value = float(line.split("=")[1].strip())
                            elif line.strip().startswith("armor_value"):
                                module.mp_max_strength = float(line.split("=")[1].strip())
                        if build_cost_resources_section:
                            if line.strip().startswith("steel"):
                                module.res_steel = int(line.split("=")[1].strip())
                            elif line.strip().startswith("chromium"):
                                module.res_chromium = int(line.split("=")[1].strip())
            except:
                print("\nAn Error has occured becuse of line:\n%s"%line)
            if "{" in line or "}" in line:
                for element in list(line.strip()):
                    if "{" in element:
                        indintation +=1
                    elif "}" in element:
                        indintation -=1
                        if indintation == 1:
                            if newModule:
                                if module.name in surface_gun_list:
                                    pass
                                else:
                                    surface_gun_list.append(module.name)
                                    if capitalShipGun:
                                        capital_gun_batteries_array.append(module)
                                        capitalShipGun = False
                                    elif cruiserShipGun:
                                        cruiser_gun_batteries_array.append(module)
                                        cruiserShipGun = False
                                    elif flightDeck:
                                        carrier_flight_deck_array.append(module)
                                        flightDeck = False
                                    elif submarineDeckGun:
                                        submarine_deck_gun_array.append(module)
                                        submarineDeckGun = False
                                newModule = False
                        elif indintation == 2:
                            add_stats_section = False
                            add_average_stats_section = False
                            multiply_stats_section = False
                            build_cost_resources_section = False
                    elif "#" in element:
                        break
            

    pass

GetModuleData()
#create 2x2 Capital when they don't exist
calaber_list_2x2 = []
capital_gun_batteries_array_2x2 = []
for gun in capital_gun_batteries_array:
    if "2x2" in gun.name and gun.caliber not in calaber_list_2x2:
        calaber_list_2x2.append(gun.caliber)
    i=0
for gun in capital_gun_batteries_array:
    if gun.caliber not in calaber_list_2x2:
       if "2x4" in gun.name:
            turrets = copy.deepcopy(gun)
            turrets.name = turrets.name.rstrip("4") + "2"
            turrets.category = turrets.category.rstrip("4") + "2"
            turrets.gui_category = turrets.gui_category.rstrip("4") + "2"
            if turrets.parent != "":
                turrets.parent = turrets.parent.rstrip("4")+"2"

            turrets.numberGuns = turrets.numberGuns/2
            turrets.numberTurrets = turrets.numberTurrets/2
            turrets.manpower = int(turrets.manpower/2)
            turrets.add_build_cost_ic = turrets.add_build_cost_ic/2
            turrets.add_max_strength = turrets.add_max_strength/2
            turrets.add_hg_attack = turrets.add_hg_attack/2
            turrets.add_supply_consumption = turrets.add_supply_consumption/2
            turrets.add_surface_visibility = turrets.add_surface_visibility/2
            turrets.mp_build_cost_ic = turrets.mp_build_cost_ic/2
            turrets.mp_reliability = turrets.mp_reliability/2
            turrets.mp_naval_speed = turrets.mp_naval_speed/2
            turrets.mp_fuel_consumption = turrets.mp_fuel_consumption/2
            turrets.dismantle_cost_ic = turrets.dismantle_cost_ic/2
            
            capital_gun_batteries_array_2x2.append(turrets)
    i=0
#create 2x1, 3x1, and 4x1 Capatal
for gun in capital_gun_batteries_array:
    if gun.name.find("3x2") >-1 or gun.name.find("4x2") >-1:
        single = copy.deepcopy(gun)
        single.name = single.name.rstrip("2")
        single.name =  single.name + "1"
        single.category = single.category.rstrip("2")
        single.category = single.category + "1"
        single.gui_category = single.gui_category.rstrip("2")
        single.gui_category = single.gui_category + "1"
        if single.parent != "":
            single.parent = single.parent.rstrip("2")+"1"

        single.numberGuns = single.numberGuns/2
        single.numberTurrets = single.numberTurrets/2
        single.manpower = int(single.manpower/2)
        single.add_build_cost_ic = single.add_build_cost_ic/2
        single.add_max_strength = single.add_max_strength/2
        single.add_hg_attack = single.add_hg_attack/2
        single.add_supply_consumption = single.add_supply_consumption/2
        single.add_surface_visibility = single.add_surface_visibility/2
        single.mp_build_cost_ic = single.mp_build_cost_ic/2
        single.mp_reliability = single.mp_reliability/2
        single.mp_naval_speed = single.mp_naval_speed/2
        single.mp_fuel_consumption = single.mp_fuel_consumption/2
        single.dismantle_cost_ic = single.dismantle_cost_ic/2

        capital_gun_batteries_array_singles.append(single)
    elif gun.name.find("2x4") >-1:
        single = copy.deepcopy(gun)
        single.name = single.name.rstrip("4")
        single.name =  single.name + "1"
        single.category = single.category.rstrip("4")
        single.category = single.category + "1"
        single.gui_category = single.gui_category.rstrip("4")
        single.gui_category = single.gui_category + "1"
        if single.parent != "":
            single.parent = single.parent.rstrip("4")+"1"

        single.numberGuns = single.numberGuns/4
        single.numberTurrets = single.numberTurrets/4
        single.manpower = int(single.manpower/4)
        single.add_build_cost_ic = single.add_build_cost_ic/4
        single.add_max_strength = single.add_max_strength/4
        single.add_hg_attack = single.add_hg_attack/4
        single.add_supply_consumption = single.add_supply_consumption/4
        single.add_surface_visibility = single.add_surface_visibility/4
        single.mp_build_cost_ic = single.mp_build_cost_ic/4
        single.mp_reliability = single.mp_reliability/4
        single.mp_naval_speed = single.mp_naval_speed/4
        single.mp_fuel_consumption = single.mp_fuel_consumption/4
        single.dismantle_cost_ic = single.dismantle_cost_ic/4

        capital_gun_batteries_array_singles.append(single)

i=0

#add single guns
capital_gun_batteries_array += capital_gun_batteries_array_singles
capital_gun_batteries_array += capital_gun_batteries_array_2x2
i=0
#create 3x1_2x1 and 4x1_2x1 Capatal
capital_gun_batteries_array_Xx1_2x1 = []
for gun1 in capital_gun_batteries_array_singles:
    if gun1.name.endswith("3x1") or gun1.name.endswith("4x1"):
        for gun2 in capital_gun_batteries_array_singles:
            if gun2.name.endswith("2x1") and gun1.level == gun2.level and gun1.caliber == gun2.caliber:
                i +=1
                hybridGun = copy.deepcopy(gun1)
                #print("%s , %s" %(gun1.caliber,gun2.caliber))   
                hybridGun.numberGuns += 2
                hybridGun.name = hybridGun.name + "_2x1"
                hybridGun.category = hybridGun.category + "_2x1"
                hybridGun.gui_category = hybridGun.gui_category + "_2x1"
                if hybridGun.parent != "":
                    hybridGun.parent += "_2x1"
                hybridGun.manpower += int(gun2.manpower)
                hybridGun.add_build_cost_ic += gun2.add_build_cost_ic
                hybridGun.add_max_strength += gun2.add_max_strength
                hybridGun.add_hg_attack += gun2.add_hg_attack
                hybridGun.add_supply_consumption += gun2.add_supply_consumption
                hybridGun.add_surface_visibility += gun2.add_surface_visibility
                hybridGun.mp_build_cost_ic += gun2.mp_build_cost_ic
                hybridGun.mp_reliability += gun2.mp_reliability
                hybridGun.mp_naval_speed += gun2.mp_naval_speed
                hybridGun.mp_fuel_consumption += gun2.mp_fuel_consumption
                hybridGun.dismantle_cost_ic += gun2.dismantle_cost_ic
                hybridGun.ic_one_turret_a += gun2.ic_one_turret
                

                capital_gun_batteries_array.append(hybridGun)
                capital_gun_batteries_array_Xx1_2x1.append(hybridGun)
                #print(hybridGun.name)

i=0
#create 2x1, 3x1, 4x1, x02, x03, and DP x04 Cruiser
cruiser_gun_batteries_array_misc = []
for gun in cruiser_gun_batteries_array:
    if gun.name.find("2x2") >-1 or gun.name.find("3x2") >-1 or gun.name.find("4x2") >-1:
        single = copy.deepcopy(gun)
        single.numberGuns = single.numberGuns/2
        single.name = single.name.rstrip("2")
        single.name =  single.name + "1"
        single.category = single.category.rstrip("2")
        single.category = single.category + "1"
        single.gui_category = single.gui_category.rstrip("2")
        single.gui_category = single.gui_category + "1"
        if single.parent != "":
            single.parent = single.parent.rstrip("2") + "1"
        single.manpower = int(single.manpower/2)
        single.add_build_cost_ic = single.add_build_cost_ic/2
        single.add_max_strength = single.add_max_strength/2
        single.add_hg_attack = single.add_hg_attack/2
        single.add_lg_attack = single.add_lg_attack/2
        single.add_anti_air_attack = single.add_anti_air_attack/2
        single.add_supply_consumption = single.add_supply_consumption/2
        single.add_surface_visibility = single.add_surface_visibility/2
        single.mp_build_cost_ic = single.mp_build_cost_ic/2
        single.mp_reliability = single.mp_reliability/2
        single.mp_naval_speed = single.mp_naval_speed/2
        single.mp_fuel_consumption = single.mp_fuel_consumption/2
        single.dismantle_cost_ic = single.dismantle_cost_ic/2
        single.numberTurrets = 1
        cruiser_gun_batteries_array_temp.append(single)
    elif "x04" in gun.name or "x06" in gun.name or ("x08" in gun.name and gun.dualPurpse):
        single2 = copy.deepcopy(gun)
        
        if "x04" in gun.name:
            single2.numberGuns = 2
            single2.name = single2.name.replace("x04","x02")
            single2.category = single2.category.replace("x04","x02")
            single2.gui_category = single2.gui_category.replace("x04","x02")
            if single2.parent != "":
                single2.parent = single2.parent.replace("x04","x02")
        elif "x06" in gun.name:
            single2.numberGuns = 3
            single2.name = single2.name.replace("x06","x03")
            single2.category = single2.category.replace("x06","x03")
            single2.gui_category = single2.gui_category.replace("x06","x03")
            if single2.parent != "":
                single2.parent = single2.parent.replace("x06","x03")
        elif "x08" in gun.name:
            single2.numberGuns = 4
            single2.name = single2.name.replace("x08","x04")
            single2.category = single2.category.replace("x08","x04")
            single2.gui_category = single2.gui_category.replace("x08","x04")
            if single2.parent != "":
                single2.parent = single2.parent.replace("x08","x04")
        single2.manpower = int(single2.manpower/2)
        single2.add_build_cost_ic = single2.add_build_cost_ic/2
        single2.add_max_strength = single2.add_max_strength/2
        single2.add_hg_attack = single2.add_hg_attack/2
        single2.add_lg_attack = single2.add_lg_attack/2
        single2.add_anti_air_attack = single2.add_anti_air_attack/2
        single2.add_supply_consumption = single2.add_supply_consumption/2
        single2.add_surface_visibility = single2.add_surface_visibility/2
        single2.mp_build_cost_ic = single2.mp_build_cost_ic/2
        single2.mp_reliability = single2.mp_reliability/2
        single2.mp_naval_speed = single2.mp_naval_speed/2
        single2.mp_fuel_consumption = single2.mp_fuel_consumption/2
        single2.dismantle_cost_ic = single2.dismantle_cost_ic/2

        cruiser_gun_batteries_array_temp.append(single2)
        cruiser_gun_batteries_array_misc.append(single2)
    if "x08" in gun.name and gun.dualPurpse:
        single2 = copy.deepcopy(gun)
        single2.numberGuns = 2
        single2.name = single2.name.replace("x08","x02")
        single2.category = single2.category.replace("x08","x02")
        single2.gui_category = single2.gui_category.replace("x08","x02")
        if single2.parent != "":
            single2.parent = single2.parent.replace("x08","x02")
        single2.manpower = int(single2.manpower/4)
        single2.add_build_cost_ic = single2.add_build_cost_ic/4
        single2.add_max_strength = single2.add_max_strength/4
        single2.add_hg_attack = single2.add_hg_attack/4
        single2.add_lg_attack = single2.add_lg_attack/4
        single2.add_anti_air_attack = single2.add_anti_air_attack/4
        single2.add_supply_consumption = single2.add_supply_consumption/4
        single2.add_surface_visibility = single2.add_surface_visibility/4
        single2.mp_build_cost_ic = single2.mp_build_cost_ic/4
        single2.mp_reliability = single2.mp_reliability/4
        single2.mp_naval_speed = single2.mp_naval_speed/4
        single2.mp_fuel_consumption = single2.mp_fuel_consumption/4
        single2.dismantle_cost_ic = single2.dismantle_cost_ic/4

        cruiser_gun_batteries_array_temp.append(single2)
        cruiser_gun_batteries_array_misc.append(single2)
i=0
#create x05 and dp x05 
for gun in cruiser_gun_batteries_array_temp:
    if "x02" in gun.name:
        for gun2 in cruiser_gun_batteries_array_temp:
            if "x03" in gun2.name:
                if gun.caliber == gun2.caliber and gun.level == gun2.level:
                    single2 = copy.deepcopy(gun2)
                    single2.numberGuns = 5
                    single2.name = single2.name.replace("x03","x05")
                    single2.category = single2.category.replace("x03","x05")
                    single2.gui_category = single2.gui_category.replace("x03","x05")
                    if single2.parent != "":
                        single2.parent = single2.parent.replace("x03","x05")
                    single2.manpower = int(single2.manpower + gun.manpower)
                    single2.add_build_cost_ic = single2.add_build_cost_ic + gun.add_build_cost_ic
                    single2.add_max_strength = single2.add_max_strength + gun.add_max_strength
                    single2.add_hg_attack = single2.add_hg_attack + gun.add_hg_attack
                    single2.add_lg_attack = single2.add_lg_attack + gun.add_lg_attack
                    single2.add_anti_air_attack = single2.add_anti_air_attack + gun.add_anti_air_attack
                    single2.add_supply_consumption = single2.add_supply_consumption + gun.add_supply_consumption
                    single2.add_surface_visibility = single2.add_surface_visibility + gun.add_surface_visibility
                    single2.mp_build_cost_ic = single2.mp_build_cost_ic + gun.mp_build_cost_ic
                    single2.mp_reliability = single2.mp_reliability + gun.mp_reliability
                    single2.mp_naval_speed = single2.mp_naval_speed + gun.mp_naval_speed
                    single2.mp_fuel_consumption = single2.mp_fuel_consumption + gun.mp_fuel_consumption
                    single2.dismantle_cost_ic = single2.dismantle_cost_ic + gun.dismantle_cost_ic

                    cruiser_gun_batteries_array_temp.append(single2)
                    cruiser_gun_batteries_array_misc.append(single2)
i=0          
#create x09 and DP x09
for gun in cruiser_gun_batteries_array:
    if False:
        if gun.name.find("x06") >-1:
            #print(gun.name)
            x09 = copy.deepcopy(gun)
            x09.name = x09.name.rstrip("x06")
            x09.name = x09.name + "x09"
            x09.category = x09.category.rstrip("x06")
            x09.category = x09.category + "x09"
            x09.gui_category = x09.gui_category.rstrip("x06")
            x09.gui_category = x09.gui_category + "x09"
            if x09.parent != "":
                x09.parent = x09.parent.replace("x06","x09")

            #x09.numberTurrets += x09.numberTurrets/2
            x09.manpower += int(x09.manpower * 1.5)
            x09.numberGuns += x09.numberGuns * 1.5
            x09.add_build_cost_ic += x09.add_build_cost_ic * 1.5
            x09.add_max_strength += x09.add_max_strength * 1.5
            x09.add_hg_attack += x09.add_hg_attack * 1.5
            x09.add_lg_attack += x09.add_lg_attack * 1.5
            x09.add_anti_air_attack += x09.add_anti_air_attack * 1.5
            x09.add_supply_consumption += x09.add_supply_consumption * 1.5
            x09.add_surface_visibility += x09.add_surface_visibility * 1.5
            x09.mp_build_cost_ic += x09.mp_build_cost_ic * 1.5
            x09.mp_reliability += x09.mp_reliability * 1.5
            x09.mp_naval_speed += x09.mp_naval_speed * 1.5
            x09.mp_fuel_consumption += x09.mp_fuel_consumption * 1.5
            x09.dismantle_cost_ic += x09.dismantle_cost_ic * 1.5

            cruiser_gun_batteries_array_temp.append(x09)
i=0
#create size 10 hangers
for hanger in carrier_flight_deck_array:
    if "_020" in hanger.name:
        fligt_deck = copy.deepcopy(hanger)
        fligt_deck.name = fligt_deck.name.replace("_020","_010")
        fligt_deck.category = fligt_deck.category.replace("_020","_010")

        fligt_deck.manpower = int(fligt_deck.manpower*0.569498)
        fligt_deck.add_build_cost_ic = fligt_deck.add_build_cost_ic*0.6129
        fligt_deck.add_max_strength = fligt_deck.add_max_strength*0.42857
        fligt_deck.add_fuel_consumption = fligt_deck.add_fuel_consumption*0.6667
        fligt_deck.add_supply_consumption = fligt_deck.add_supply_consumption*0.53
        fligt_deck.add_surface_visibility = fligt_deck.add_surface_visibility*.6129
        fligt_deck.add_carrier_size = int(fligt_deck.add_carrier_size*.51)

        fligt_deck.mp_build_cost_ic = fligt_deck.mp_build_cost_ic*.3897
        fligt_deck.mp_reliability = fligt_deck.mp_reliability*.5
        fligt_deck.mp_naval_speed = fligt_deck.mp_naval_speed*.554
        fligt_deck.mp_fuel_consumption = fligt_deck.mp_fuel_consumption*.25

        fligt_deck.dismantle_cost_ic = fligt_deck.dismantle_cost_ic*.95

        tmp_carrier_flight_deck_array.append(fligt_deck)
i=0
#Add tmp arrays together
cruiser_gun_batteries_array += cruiser_gun_batteries_array_temp
carrier_flight_deck_array += tmp_carrier_flight_deck_array

x=0

# Matrix Combiner Capital
for gun in capital_gun_batteries_array:
    for deck in carrier_flight_deck_array:
        #Addes Exceptions to matrix        
        #NEW
        if gun.name.endswith("2x4") or gun.name.endswith("2x3") or gun.name.endswith("3x2") or gun.name.endswith("4x2") or "x1_2x" in gun.name:
            continue
        elif (gun.name.endswith("2x2") or gun.name.endswith("4x1")) and deck.name.endswith("30"):
            continue
        elif deck.name.endswith("10"):
            continue
        else:
            Matrix_combiner(gun, deck, capital_hybrid_array)
            x +=1
i=0

# Matrix Combiner Cruiser
for gun in cruiser_gun_batteries_array:
    for deck in carrier_flight_deck_array:
        #Addes Exceptions to matrix
        #New
        if gun.name.endswith("4x2") or gun.name.endswith("x08") or gun.name.endswith("x09") or "x06" in gun.name or "x04" in gun.name or "x05" in gun.name:
            continue
        elif deck.name.endswith("25") or deck.name.endswith("30"):
            continue
        elif("x02" in gun.name or "x03" in gun.name or "_PB_" in gun.name) and deck.name.endswith("20"):
            continue
        else:
            Matrix_combiner(gun, deck, cruiser_hybrid_array)
            x +=1
total = x
i=0
x+=len(capital_gun_batteries_array_2x2)
x+=len(capital_gun_batteries_array_Xx1_2x1)
x+=len(capital_gun_batteries_array_singles)
print("%s total surface modules"%x)

#Output to File
Module_outputer(capital_hybrid_array, "Output\\modules\\Lic_capital_hybrid.txt")
Module_outputer(cruiser_hybrid_array, "Output\\modules\\Lic_cruiser_hybrid.txt")

#Tech tree & Events
#Create copy of capital_hybrid_array and cruiser_hybrid_array
#create tech based on where guns were, carrier tech, AHL/CHL
#remove each item when placed in techs
#print results after completion to find any I missed
#
#Techs:                         Modules    calaber_level
#   improved_dp_light_battery_2-   DP_5_2                       
#   advanced_dp_light_battery_2-   DP_5_3                       
#   improved_dp_medium_battery -   DP_5.5_2                     
#   advanced_dp_medium_battery -   DP_5.5_3                     
#   modern_dp_medium_battery   -   DP_6_3                       
#   basic_battery              -   11_1 12_1 5_1 5.5_1 6_1
#   improved_light_battery_2   -   5_2
#   advanced_light_battery_2   -   5_3
#   improved_medium_battery    -   5.5_2 6_2
#   advanced_medium_battery    -   5.5_3 6_3
#   modern_medium_battery      -   6_4
#   basic_medium_battery_2     -   8_1
#   improved_medium_battery_2  -   8_2
#   advanced_medium_battery_2  -   8_3
#   modern_medium_battery_2    -   8_4
#   improved_heavy_battery     -   11_2 12_2
#   advanced_heavy_battery     -   11_3 12_3
#   basic_heavy_battery_2      -   13_1 14_1
#   improved_heavy_battery_2   -   13_2 14_2
#   advanced_heavy_battery_2   -   13_3 14_3
#   basic_heavy_battery_3      -   15_1 16_1
#   improved_heavy_battery_3   -   15_2 16_2
#   advanced_heavy_battery_3   -   15_3 16_3
#   improved_heavy_battery_4   -   18_2
#   advanced_heavy_battery_4   -   18_3
#   improved_heavy_battery_5   -   20_2
#   advanced_heavy_battery_5   -   20_3
#                               						27
#   basic_ship_hull_carrier    -   CHL
#   armoured_hangar            -   AHL						2
#                               Capital     Cruiser
#   airplane_launcher          -    15 20        10
#   improved_airplane_launcher -    25           15
#   advanced_airplane_launcher -    30           20		3		162 techs

#   BICE
#   nrm_battery_improved_dp_5h -    DP_5.5_2    #   nrm_battery_improved_dp_5  -    DP_5_2
#   nrm_battery_advanced_dp_5h -    DP_5.5_3    #   nrm_battery_advanced_dp_5  -    DP_5_3
#   nrm_battery_advanced_dp_6  -    DP_6_3
#   nrm_battery_modern_dp_6    -    DP_6_4
#   nrm_battery_basic          -    5_1     #   nrm_battery_early_5h       -    5.5_1 
#   nrm_battery_improved_5     -    5_2     #   nrm_battery_improved_5h    -    5.5_2   
#   nrm_battery_advanced_5     -    5_3     #   nrm_battery_advanced_5h    -    5.5_3   
#   nrm_battery_early_6        -    6_1
#   nrm_battery_improved_6     -    6_2
#   nrm_battery_advanced_6     -    6_3
#   nrm_battery_modern_6       -    6_4
#   nrm_battery_early_8        -    8_1
#   nrm_battery_improved_8     -    8_2
#   nrm_battery_advanced_8     -    8_3
#   nrm_battery_modern_8       -    8_4
#   nrm_battery_early_11       -    11_1    #   nrm_battery_early_12       -    12_1
#   nrm_battery_improved_11    -    11_2    #   nrm_battery_improved_12    -    12_2
#   nrm_battery_advanced_11    -    11_3    #   nrm_battery_advanced_12    -    12_3
#   nrm_battery_early_13       -    13_1    #   nrm_battery_early_14       -    14_1
#   nrm_battery_improved_13    -    13_2    #   nrm_battery_improved_14    -    14_2
#   nrm_battery_advanced_13    -    13_3    #   nrm_battery_advanced_14    -    14_3
#   nrm_battery_early_15       -    15_1    #   nrm_battery_early_16       -    16_1
#   nrm_battery_improved_15    -    15_2    #   nrm_battery_improved_16    -    16_2
#   nrm_battery_advanced_15    -    15_3    #   nrm_battery_advanced_16    -    16_3
#   nrm_battery_improved_18    -    18_2
#   nrm_battery_advanced_18    -    18_3
#   nrm_battery_improved_20    -    20_2
#   nrm_battery_advanced_20    -    20_3             28
merged_hybrid_array = copy.deepcopy(capital_hybrid_array) + copy.deepcopy(cruiser_hybrid_array)

#Guns BICE
gunTechs_set_BICE = {
    "nrm_battery_improved_dp_4":[],
    "nrm_battery_advanced_dp_4":[],
    "nrm_battery_early_5h":[],
    "nrm_battery_improved_dp_5h":[],
    "nrm_battery_advanced_dp_5h":[],
    "nrm_battery_improved_dp_5":[],
    "nrm_battery_advanced_dp_5":[],
    "nrm_battery_advanced_dp_6":[],
    "nrm_battery_modern_dp_6":[],
    "nrm_battery_early_5h":[],
    "nrm_battery_improved_5h":[],
    "nrm_battery_advanced_5h":[],
    "nrm_battery_improved_4":[],
    "nrm_battery_advanced_4":[],
    "nrm_battery_improved_5":[],
    "nrm_battery_advanced_5":[],
    "nrm_battery_early_6":[],
    "nrm_battery_improved_6":[],
    "nrm_battery_advanced_6":[],
    "nrm_battery_modern_6":[],
    "nrm_battery_early_8":[],
    "nrm_battery_improved_8":[],
    "nrm_battery_advanced_8":[],
    "nrm_battery_modern_8":[],
    "nrm_battery_early_11":[],
    "nrm_battery_improved_11":[],
    "nrm_battery_advanced_11":[],
    "nrm_battery_early_12":[],
    "nrm_battery_improved_12":[],
    "nrm_battery_advanced_12":[],
    "nrm_battery_early_13":[],
    "nrm_battery_improved_13":[],
    "nrm_battery_advanced_13":[],
    "nrm_battery_early_14":[],
    "nrm_battery_improved_14":[],
    "nrm_battery_advanced_14":[],
    "nrm_battery_early_15":[],
    "nrm_battery_improved_15":[],
    "nrm_battery_advanced_15":[],
    "nrm_battery_early_16":[],
    "nrm_battery_improved_16":[],
    "nrm_battery_advanced_16":[],
    "nrm_battery_improved_18":[],
    "nrm_battery_advanced_18":[],
    "nrm_battery_improved_20":[],
    "nrm_battery_advanced_20":[],
    "nrm_battery_basic":[]
    }

#Guns
gunTechs_set = {
    "basic_battery":[],
    "improved_light_battery":[],
    "improved_light_battery_2":[],
    "advanced_light_battery":[],
    "advanced_light_battery_2":[],
    "improved_dp_light_battery":[],
    "improved_dp_light_battery_2":[],
    "advanced_dp_light_battery":[],
    "advanced_dp_light_battery_2":[],
    "improved_medium_battery":[],
    "advanced_medium_battery":[],
    "modern_medium_battery":[],
    "improved_dp_medium_battery":[],
    "advanced_dp_medium_battery":[],
    "modern_dp_medium_battery":[],
    "basic_medium_battery_2":[],
    "improved_medium_battery_2":[],
    "advanced_medium_battery_2":[],
    "modern_medium_battery_2":[],
    "improved_heavy_battery":[],
    "advanced_heavy_battery":[],
    "basic_heavy_battery_2":[],
    "improved_heavy_battery_2":[],
    "advanced_heavy_battery_2":[],
    "basic_heavy_battery_3":[],
    "improved_heavy_battery_3":[],
    "advanced_heavy_battery_3":[],
    "improved_heavy_battery_4":[],
    "advanced_heavy_battery_4":[],
    "improved_heavy_battery_5":[],
    "advanced_heavy_battery_5":[]
    }


#Hangers | Launcher
hangerTechs_set = {
    "basic_ship_hull_carrier|airplane_launcher":[],
    "basic_ship_hull_carrier|improved_airplane_launcher":[],
    "basic_ship_hull_carrier|advanced_airplane_launcher":[],
    "armoured_hangar|airplane_launcher":[],
    "armoured_hangar|improved_airplane_launcher":[],
    "armoured_hangar|advanced_airplane_launcher":[]
    }



#Break each module up into individule techs for each Guns, Launchers, and Hangers
def gun_selecor(module, tech_set):
    if BICE:
        if "DP_4_2" in module.name:
            tech_set["nrm_battery_improved_dp_4"].append(module)
        elif "DP_4_3" in module.name:
            tech_set["nrm_battery_advanced_dp_4"].append(module)
        elif "DP_5h_1" in module.name:
            tech_set["nrm_battery_early_5h"].append(module)
        elif "DP_5h_2" in module.name:
            tech_set["nrm_battery_improved_dp_5h"].append(module)
        elif "DP_5h_3" in module.name:
            tech_set["nrm_battery_advanced_dp_5h"].append(module)
        elif "DP_5_2" in module.name:
            tech_set["nrm_battery_improved_dp_5"].append(module)
        elif "DP_5_3" in module.name:
            tech_set["nrm_battery_advanced_dp_5"].append(module)
        elif "DP_6_3" in module.name:
            tech_set["nrm_battery_advanced_dp_6"].append(module)
        elif "DP_6_4" in module.name:
            tech_set["nrm_battery_modern_dp_6"].append(module)
        elif "battery_4_2" in module.name:
            tech_set["nrm_battery_improved_4"].append(module)
        elif "battery_4_3" in module.name:
            tech_set["nrm_battery_advanced_4"].append(module)
        elif "battery_5_2" in module.name:
            tech_set["nrm_battery_improved_5"].append(module)
        elif "battery_5_3" in module.name:
            tech_set["nrm_battery_advanced_5"].append(module)
        elif "battery_5h_2" in module.name:
            tech_set["nrm_battery_improved_5h"].append(module)
        elif "battery_5h_3" in module.name:
            tech_set["nrm_battery_advanced_5h"].append(module)
        elif "battery_6_1" in module.name:
            tech_set["nrm_battery_early_6"].append(module)
        elif "battery_6_2" in module.name:
            tech_set["nrm_battery_improved_6"].append(module)
        elif "battery_6_3" in module.name:
            tech_set["nrm_battery_advanced_6"].append(module)
        elif "battery_6_4" in module.name:
            tech_set["nrm_battery_modern_6"].append(module)
        elif "battery_8_1" in module.name:
            tech_set["nrm_battery_early_8"].append(module)
        elif "battery_8_2" in module.name:
            tech_set["nrm_battery_improved_8"].append(module)
        elif "battery_8_3" in module.name:
            tech_set["nrm_battery_advanced_8"].append(module)
        elif "battery_8_4" in module.name:
            tech_set["nrm_battery_modern_8"].append(module)
        elif "_11_1" in module.name:
            tech_set["nrm_battery_early_11"].append(module)
        elif "_11_2" in module.name:
            tech_set["nrm_battery_improved_11"].append(module)
        elif "_11_3" in module.name:
            tech_set["nrm_battery_advanced_11"].append(module)
        elif "_12_1" in module.name:
            tech_set["nrm_battery_early_12"].append(module)
        elif "_12_2" in module.name:
            tech_set["nrm_battery_improved_12"].append(module)
        elif "_12_3" in module.name:
            tech_set["nrm_battery_advanced_12"].append(module)
        elif "_13_1" in module.name:
            tech_set["nrm_battery_early_13"].append(module)
        elif "_13_2" in module.name:
            tech_set["nrm_battery_improved_13"].append(module)
        elif "_13_3" in module.name:
            tech_set["nrm_battery_advanced_13"].append(module)
        elif "_14_1" in module.name:
            tech_set["nrm_battery_early_14"].append(module)
        elif "_14_2" in module.name:
            tech_set["nrm_battery_improved_14"].append(module)
        elif "_14_3" in module.name:
            tech_set["nrm_battery_advanced_14"].append(module)
        elif "_15_1" in module.name:
            tech_set["nrm_battery_early_15"].append(module)
        elif "_15_2" in module.name:
            tech_set["nrm_battery_improved_15"].append(module)
        elif "_15_3" in module.name:
            tech_set["nrm_battery_advanced_15"].append(module)
        elif "_16_1" in module.name:
            tech_set["nrm_battery_early_16"].append(module)
        elif "_16_2" in module.name:
            tech_set["nrm_battery_improved_16"].append(module)
        elif "_16_3" in module.name:
            tech_set["nrm_battery_advanced_16"].append(module)
        elif "_18_2" in module.name:
            tech_set["nrm_battery_improved_18"].append(module)
        elif "_18_3" in module.name:
            tech_set["nrm_battery_advanced_18"].append(module)
        elif "_20_2" in module.name:
            tech_set["nrm_battery_improved_20"].append(module)
        elif "_20_3" in module.name:
            tech_set["nrm_battery_advanced_20"].append(module)
        else:
            tech_set["nrm_battery_basic"].append(module)

    else:
        #improved_dp_light_battery_2    Get DP out of the wy first
        if module.name.find("DP_5_2") >-1:
            tech_set["improved_dp_light_battery_2"].append(module)
        elif module.name.find("DP_5_3") >-1:
            tech_set["advanced_dp_light_battery_2"].append(module)
        elif module.name.find("DP_5.5_2") >-1 or "DP_5h_2" in module.name:
            tech_set["improved_dp_medium_battery"].append(module)
        elif module.name.find("DP_5.5_3") >-1 or module.name.find("DP_6_3") >-1 or module.name.find("DP_5h_3") >-1:
            tech_set["advanced_dp_medium_battery"].append(module)
        elif module.name.find("DP_6_4") >-1:
            tech_set["modern_dp_medium_battery"].append(module)
        elif "DP_4_2" in module.name:
            tech_set["improved_dp_light_battery"].append(module)
        elif "DP_4_3" in module.name:
            tech_set["advanced_dp_light_battery"].append(module)
        elif module.name.find("11_1") >-1 or module.name.find("12_1") >-1 or module.name.find("_5_1") >-1 or module.name.find("_5.5_1") >-1 or module.name.find("_6_1") >-1 or "_5h_1" in module.name or "_4_1" in module.name:
            tech_set["basic_battery"].append(module)
        elif "_4_2" in module.name:
            tech_set["improved_light_battery"].append(module)
        elif "_4_3" in module.name:
            tech_set["advanced_light_battery"].append(module)
        elif module.name.find("_5_2") >-1:
            tech_set["improved_light_battery_2"].append(module)
        elif module.name.find("_5_3") >-1:
            tech_set["advanced_light_battery_2"].append(module)
        elif module.name.find("_5.5_2") >-1 or module.name.find("_6_2") >-1 or module.name.find("_5h_2") >-1:
            tech_set["improved_medium_battery"].append(module)
        elif module.name.find("_5.5_3") >-1 or module.name.find("_6_3") >-1 or module.name.find("_5h_3") >-1:
            tech_set["advanced_medium_battery"].append(module)
        elif module.name.find("_6_4") >-1:
            tech_set["modern_medium_battery"].append(module)
        elif module.name.find("_8_1") >-1:
            tech_set["basic_medium_battery_2"].append(module)
        elif module.name.find("_8_2") >-1:
            tech_set["improved_medium_battery_2"].append(module)
        elif module.name.find("_8_3") >-1:
            tech_set["advanced_medium_battery_2"].append(module)
        elif module.name.find("_8_4") >-1:
            tech_set["modern_medium_battery_2"].append(module)
        elif module.name.find("11_2") >-1 or module.name.find("12_2") >-1:
            tech_set["improved_heavy_battery"].append(module)
        elif module.name.find("11_3") >-1 or module.name.find("12_3") >-1:
            tech_set["advanced_heavy_battery"].append(module)
        elif module.name.find("13_1") >-1 or module.name.find("14_1") >-1:
            tech_set["basic_heavy_battery_2"].append(module)
        elif module.name.find("13_2") >-1 or module.name.find("14_2") >-1:
            tech_set["improved_heavy_battery"].append(module)
        elif module.name.find("13_3") >-1 or module.name.find("14_3") >-1:
            tech_set["advanced_heavy_battery_2"].append(module)
        elif module.name.find("15_1") >-1 or module.name.find("16_1") >-1:
            tech_set["basic_heavy_battery_3"].append(module)
        elif module.name.find("15_2") >-1 or module.name.find("16_2") >-1:
            tech_set["improved_heavy_battery_3"].append(module)
        elif module.name.find("15_3") >-1 or module.name.find("16_3") >-1:
            tech_set["advanced_heavy_battery_3"].append(module)
        elif module.name.find("18_2") >-1:
            tech_set["improved_heavy_battery_4"].append(module)
        elif module.name.find("18_3") >-1:
            tech_set["advanced_heavy_battery_4"].append(module)
        elif module.name.find("20_2") >-1:
            tech_set["improved_heavy_battery_5"].append(module)
        elif module.name.find("20_3") >-1:
            tech_set["advanced_heavy_battery_5"].append(module)
    pass

i=0

for module in merged_hybrid_array:
    #basic_ship_hull_carrier
    if module.name.find("_CHL_") >-1:
        if module.name.find("_010") >-1 or (module.name.find("_020") >-1 and module.name.find("capital") >-1):
            hangerTechs_set["basic_ship_hull_carrier|airplane_launcher"].append(module)
        elif module.name.find("_030") >-1 or (module.name.find("_020") >-1 and module.name.find("cruiser") >-1):
            hangerTechs_set["basic_ship_hull_carrier|improved_airplane_launcher"].append(module)
        if BICE:
            gun_selecor(module,gunTechs_set_BICE)
        else:
            gun_selecor(module,gunTechs_set)
i=0


#Key value pair         probably the best way to mearge them together

mergedTech_set = {}

def techNamer(gun, hanger, launcher):
    return ("%s_%s_%s"%(gun,hanger,launcher))

techName = ""
techEvents = []

i=0

#Get Rid of hangers loop 
#find a way of merging hangers into launchers
# 3 hours to 10 sec improvment!!!

if BICE:
    for key1,val1 in gunTechs_set_BICE.items():
        for key2,val2 in hangerTechs_set.items():
            for guns in val1:
                for hangers in val2:
                    if (guns.name) is (hangers.name):
                        #create Tech Name
                        if "basic_ship_hull_carrier|" in key2:
                            if "|airplane_launcher" in key2:
                                techName = techNamer(key1,"converted","small")
                            elif "|improved_airplane_launcher" in key2:
                                techName = techNamer(key1,"converted","large")
                        #link techs to their tech name
                        #print(techName)
                        if techName in mergedTech_set:
                            mergedTech_set[copy.deepcopy(techName)].append(copy.deepcopy(guns.name))
                            i += 1
                        else:
                            mergedTech_set[copy.deepcopy(techName)] = [copy.deepcopy(guns.name)]
                            i += 1
                            eventStuf = DefTechEvents()
                            eventStuf.name = copy.deepcopy(techName)
                            eventStuf.gunTech = copy.deepcopy(key1)
                            if "basic_ship_hull_carrier|" in key2:
                                eventStuf.hangerTech = "basic_ship_hull_carrier"
                            elif "armoured_hangar|" in key2:
                                eventStuf.hangerTech = "armoured_hangar"

                            if "|airplane_launcher" in key2:
                                eventStuf.launcherTech = "airplane_launcher"
                            elif "|improved_airplane_launcher" in key2:
                                eventStuf.launcherTech = "improved_airplane_launcher"

                            #print("%s\t-\t%s"%(techName,(i/total)*100))
                            techEvents.append(eventStuf)
    
    #print("%s modules of %s"%(i,total)) 
else:
    for key1,val1 in gunTechs_set.items():
        for key2,val2 in hangerTechs_set.items():
            for guns in val1:
                for hangers in val2:
                    if (guns.name) is (hangers.name):
                        #create Tech Name
                        if "basic_ship_hull_carrier|" in key2:
                            if "|airplane_launcher" in key2:
                                techName = techNamer(key1,"converted","small")
                            elif "|improved_airplane_launcher" in key2:
                                techName = techNamer(key1,"converted","large")
                        #link techs to their tech name
                        #print(techName)
                        if techName in mergedTech_set:
                            mergedTech_set[copy.deepcopy(techName)].append(copy.deepcopy(guns.name))
                            i += 1
                        else:
                            mergedTech_set[copy.deepcopy(techName)] = [copy.deepcopy(guns.name)]
                            i += 1
                            eventStuf = DefTechEvents()
                            eventStuf.name = copy.deepcopy(techName)
                            eventStuf.gunTech = copy.deepcopy(key1)
                            if "basic_ship_hull_carrier|" in key2:
                                eventStuf.hangerTech = "basic_ship_hull_carrier"

                            if "|airplane_launcher" in key2:
                                eventStuf.launcherTech = "airplane_launcher"
                            elif "|improved_airplane_launcher" in key2:
                                eventStuf.launcherTech = "improved_airplane_launcher"

                            print("%s\t-\t%s"%(techName,(i/total)*100))
                            techEvents.append(eventStuf)

    #print("%s modules of %s"%(i,total))                                
i=0

# Submarine Turrets
# x02 x03 in 5 5.5
# x02 in 6 8
# x01 in 13 14 15 16
submarine_turrets = []
subGun_list = []
x=0
for gun in cruiser_gun_batteries_array:
    if "_5_" in gun.name or "_5.5_" in gun.name or "_5h_" in gun.name:
        if "x02" in gun.name or "x03" in gun.name or "x04" in gun.name or "x06" in gun.name:
            if gun.name in subGun_list:
                continue
            else:
                subGun = copy.deepcopy(gun)

                subGun.name = "nrm_submarine_battery_"
                if gun.dualPurpse:
                    subGun.name += "DP_"
                if gun.caliber == 5.5:
                    subGun.name += "5h_"
                else:
                    subGun.name += ("%g_"%subGun.caliber)
                subGun.name += ("%g_x0%g"%(subGun.level,subGun.numberGuns))


                subGun.category = "nrm_submarine_battery_light"
                subGun.gui_category = subGun.category
                #print(subGun.gui_category)
                if subGun.numberGuns == 4:
                    subGun.category += "_x2m"
                elif subGun.numberGuns == 6:
                    subGun.category += "_x2h"
                
                
                if subGun.parent != "":
                    subGun.parent = subGun.parent.replace("nrm_cruiser_battery","nrm_submarine_battery")

                subGun.add_build_cost_ic = subGun.add_build_cost_ic * 1.5
                subGun.mp_naval_speed = subGun.mp_naval_speed*8
                subGun.mp_build_cost_ic = subGun.mp_build_cost_ic*20
                subGun.mp_fuel_consumption = subGun.mp_fuel_consumption*1.5
                subGun.manpower = subGun.manpower/2
                subGun.add_surface_visibility = subGun.add_surface_visibility*6
                #deck gun sub_visibility = 0.00199074074074074074074074074074 * caliber^3
                subGun.add_sub_visibility = 0.00199074074074074074074074074074 * subGun.caliber**3 * 1.1

                subGun.mp_reliability = subGun.mp_reliability *1.2
                subGun.add_max_strength = subGun.add_max_strength *1.5
                subGun.add_lg_attack = subGun.add_lg_attack *2
                subGun.dismantle_cost_ic = subGun.add_build_cost_ic/3
                #print(gun.av_lg_armor_piercing)
                submarine_turrets.append(subGun)
                subGun_list.append(subGun.name)
                x+=1

                #4" guns
                if "_5_" in gun.name:
                    if gun.name in subGun_list:
                        continue
                    else:
                        subGun = copy.deepcopy(gun)
                        subGun.name = "nrm_submarine_battery_"
                        if gun.dualPurpse:
                            subGun.name += ("DP_")
                        subGun.name += ("4_")
                        subGun.caliber = 4
                        subGun.name += ("%g_x0%g"%(subGun.level,subGun.numberGuns))

                        
                        if subGun.numberGuns > 3:
                            subGun.category = "nrm_submarine_battery_light_x2m"
                            subGun.gui_category = "nrm_submarine_battery_light"
                        else:
                            subGun.category = "nrm_submarine_battery_light"
                            subGun.gui_category = subGun.category

                        if subGun.parent != "":
                            subGun.parent = subGun.parent.replace("nrm_cruiser_battery","nrm_submarine_battery")

                        subGun.add_build_cost_ic = subGun.add_build_cost_ic * 1.5 * 0.512
                        subGun.mp_naval_speed = subGun.mp_naval_speed*8 * 0.512
                        subGun.mp_build_cost_ic = subGun.mp_build_cost_ic*20 * 0.512
                        subGun.mp_fuel_consumption = subGun.mp_fuel_consumption*1.5 *0.512
                        subGun.manpower = subGun.manpower/2 *0.64
                        subGun.add_surface_visibility = subGun.add_surface_visibility*6 *0.5
                        #deck gun sub_visibility = 0.00199074074074074074074074074074 * caliber^3
                        subGun.add_sub_visibility = 0.00199074074074074074074074074074 * subGun.caliber**3 * 1.1

                        subGun.mp_reliability = subGun.mp_reliability *1.2 * 0.8
                        subGun.add_max_strength = subGun.add_max_strength *1.5 * 0.512
                        subGun.add_lg_attack = subGun.add_lg_attack *2 * 0.67
                        subGun.add_anti_air_attack *= 0.67
                        subGun.dismantle_cost_ic = subGun.add_build_cost_ic/3 *0.512
                        subGun.av_lg_armor_piercing *= 0.83
                        #print(gun.av_lg_armor_piercing)
                        submarine_turrets.append(subGun)
                        subGun_list.append(subGun.name)
                        x+=1
        pass

    elif "_6_" in gun.name or "_8_" in gun.name:
        if "x02" in gun.name or ("x03" in gun.name and "_6_" in gun.name):
            if gun.name in subGun_list:
                pass
            else:
                subGun = copy.deepcopy(gun)

                subGun.name = "nrm_submarine_battery_"
                if gun.dualPurpse:
                    subGun.name += ("DP_")
                subGun.name += ("%g_"%subGun.caliber)
                subGun.name += ("%g_x0%g"%(subGun.level,subGun.numberGuns))

                subGun.category = "nrm_submarine_battery_medium"
                if gun.caliber < 5:
                    subGun.gui_category = "nrm_submarine_battery_light_medium"
                else:
                    subGun.gui_category = subGun.category

                if subGun.parent != "":
                    subGun.parent = subGun.parent.replace("nrm_cruiser_battery","nrm_submarine_battery")

                subGun.add_build_cost_ic = subGun.add_build_cost_ic * 1.5
                subGun.mp_naval_speed = subGun.mp_naval_speed*8
                subGun.mp_build_cost_ic = subGun.mp_build_cost_ic*20
                subGun.mp_fuel_consumption = subGun.mp_fuel_consumption*1.5
                subGun.manpower = subGun.manpower/2
                subGun.add_surface_visibility = subGun.add_surface_visibility*6
                subGun.add_sub_visibility = 0.00199074074074074074074074074074 * subGun.caliber**3 * 1.1
                subGun.mp_reliability = subGun.mp_reliability *1.2
                subGun.add_max_strength = subGun.add_max_strength *1.5
                subGun.add_lg_attack = subGun.add_lg_attack *2
                subGun.add_hg_attack = subGun.add_hg_attack *1.6
                subGun.dismantle_cost_ic = subGun.add_build_cost_ic/3


                #print(gun.name)
                submarine_turrets.append(subGun)
                subGun_list.append(gun.name)
                print("%s : %s"%(gun.name,gun.add_max_strength))
                x+=1
    pass
i=0
for gun in capital_gun_batteries_array:
    if "_11_" in gun.name or "_12_" in gun.name or "_13_" in gun.name or "_14_" in gun.name or "_15_" in gun.name or "_16_" in gun.name:
        if "2x4" in gun.name:
            if gun.name in subGun_list:
                continue
            else:
                single = copy.deepcopy(gun)
                single.numberGuns = single.numberGuns/8
                single.name = "nrm_submarine_battery_"
                single.name += ("%g_"%single.caliber)
                single.name += ("%g_x0%g"%(single.level,single.numberGuns))

                single.category = "nrm_submarine_battery_heavy"
                single.gui_category = single.category

                if single.parent != "":
                    single.parent = single.parent.replace("nrm_capital_battery","nrm_submarine_battery")
                    single.parent = single.parent.replace("_2x4","_x01")
                
                single.numberTurrets = single.numberTurrets/8
                single.manpower = int(single.manpower/8)
                single.add_build_cost_ic = single.add_build_cost_ic/4
                single.add_max_strength = single.add_max_strength/8
                single.add_hg_attack = single.add_hg_attack/8
                single.add_supply_consumption = single.add_supply_consumption/8
                single.add_surface_visibility = single.add_surface_visibility/4
                single.mp_build_cost_ic = single.mp_build_cost_ic/8
                single.mp_reliability = single.mp_reliability/6.7
                single.mp_naval_speed = single.mp_naval_speed/8
                single.mp_fuel_consumption = single.mp_fuel_consumption/8
                single.dismantle_cost_ic = single.dismantle_cost_ic/8

                single.add_build_cost_ic = single.add_build_cost_ic * 1.5
                single.mp_naval_speed = single.mp_naval_speed
                single.mp_build_cost_ic = single.mp_build_cost_ic*10
                single.mp_fuel_consumption = single.mp_fuel_consumption*1.5
                single.add_surface_visibility = single.add_surface_visibility*3
                single.add_sub_visibility = 0.00199074074074074074074074074074 * single.caliber**3 * 0.55
                single.manpower = single.manpower/2

                subGun.mp_reliability = subGun.mp_reliability *1.2/8
                subGun.add_max_strength = subGun.add_max_strength *1.5/8
                subGun.add_hg_attack = subGun.add_hg_attack *1.6/8
                subGun.dismantle_cost_ic = subGun.add_build_cost_ic/24
                #print(single.name)
                submarine_turrets.append(single)
                subGun_list.append(gun.name)
                x+=1
    pass
i=0

print("Tech Matrix Combiner Finished")
Tech_outputer(mergedTech_set, "Output\\technologies\\Lic_MtG_Naval_Hybrid.txt")
Event_outputer(techEvents, "Output\\events\\Lic_Hybrid_Events.txt", "Lic_surface_hybrids", "lic_tech")
#local_ship_modules(merged_hybrid_array, "Output\\localisation\\english\\Lic_Hybrid_modules_l_english.yml")
local_tech(mergedTech_set, "Output\\localisation\\english\\Lic_Hybrid_tech_l_english.yml")

Module_sub_outputer(submarine_turrets, "Output\\modules\\Lic_submarine_battery.txt")


#Submarine super firing deck guns
#Submarine Deck Guns x2
submarine_deckguns_x2 = []
for gun in submarine_deck_gun_array:
    subGun = copy.deepcopy(gun)
    subGun.name+= "_x2"
    subGun.parent+=gun.name
    subGun.numberGuns*=2
    #print(subGun.name)
    subGun.manpower*=2
    subGun.add_build_cost_ic*=2.1
    subGun.add_max_strength*=2.1
    subGun.add_lg_attack*=2
    subGun.add_supply_consumption*=2
    subGun.add_sub_visibility*=2
    subGun.mp_build_cost_ic*=2
    subGun.mp_reliability*=2
    subGun.mp_naval_speed*=2
    subGun.mp_fuel_consumption*=2

    if gun.caliber < 5:
        subGun.category = "nrm_submarine_deckgun_3-4_x2"
    elif gun.caliber < 7:
        subGun.category = "nrm_submarine_deckgun_5-6_x2"
    elif gun.caliber > 7:
        subGun.category = "nrm_submarine_deckgun_8_x2"
        subGun.add_equipment_type = "capital_ship"
        subGun.add_hg_attack=subGun.add_lg_attack
        subGun.add_lg_attack*=0.34
        subGun.av_hg_armor_piercing=subGun.av_lg_armor_piercing
        subGun.critical_parts = "damaged_heavy_guns"
        subGun.dismantle_cost_ic = 0

    submarine_deckguns_x2.append(subGun)


subGunTechs_set_BICE = {
    "nrm_battery_improved_dp_4":[],
    "nrm_battery_advanced_dp_4":[],
    "nrm_battery_early_5h":[],
    "nrm_battery_improved_dp_5h":[],
    "nrm_battery_advanced_dp_5h":[],
    "nrm_battery_improved_dp_5":[],
    "nrm_battery_advanced_dp_5":[],
    "nrm_battery_advanced_dp_6":[],
    "nrm_battery_modern_dp_6":[],
    "nrm_battery_early_5h":[],
    "nrm_battery_improved_5h":[],
    "nrm_battery_advanced_5h":[],
    "nrm_battery_improved_4":[],
    "nrm_battery_advanced_4":[],
    "nrm_battery_improved_5":[],
    "nrm_battery_advanced_5":[],
    "nrm_battery_early_6":[],
    "nrm_battery_improved_6":[],
    "nrm_battery_advanced_6":[],
    "nrm_battery_modern_6":[],
    "nrm_battery_early_8":[],
    "nrm_battery_improved_8":[],
    "nrm_battery_advanced_8":[],
    "nrm_battery_modern_8":[],
    "nrm_battery_early_11":[],
    "nrm_battery_improved_11":[],
    "nrm_battery_advanced_11":[],
    "nrm_battery_early_12":[],
    "nrm_battery_improved_12":[],
    "nrm_battery_advanced_12":[],
    "nrm_battery_early_13":[],
    "nrm_battery_improved_13":[],
    "nrm_battery_advanced_13":[],
    "nrm_battery_early_14":[],
    "nrm_battery_improved_14":[],
    "nrm_battery_advanced_14":[],
    "nrm_battery_early_15":[],
    "nrm_battery_improved_15":[],
    "nrm_battery_advanced_15":[],
    "nrm_battery_early_16":[],
    "nrm_battery_improved_16":[],
    "nrm_battery_advanced_16":[],
    "nrm_battery_improved_18":[],
    "nrm_battery_advanced_18":[],
    "nrm_battery_improved_20":[],
    "nrm_battery_advanced_20":[],
    "nrm_battery_basic":[]
}

subGunTechs_set = {
    "basic_battery":[],
    "improved_light_battery":[],
    "improved_light_battery_2":[],
    "advanced_light_battery":[],
    "advanced_light_battery_2":[],
    "improved_dp_light_battery":[],
    "improved_dp_light_battery_2":[],
    "advanced_dp_light_battery":[],
    "advanced_dp_light_battery_2":[],
    "improved_medium_battery":[],
    "advanced_medium_battery":[],
    "modern_medium_battery":[],
    "improved_dp_medium_battery":[],
    "advanced_dp_medium_battery":[],
    "modern_dp_medium_battery":[],
    "basic_medium_battery_2":[],
    "improved_medium_battery_2":[],
    "advanced_medium_battery_2":[],
    "modern_medium_battery_2":[],
    "improved_heavy_battery":[],
    "advanced_heavy_battery":[],
    "basic_heavy_battery_2":[],
    "improved_heavy_battery_2":[],
    "advanced_heavy_battery_2":[],
    "basic_heavy_battery_3":[],
    "improved_heavy_battery_3":[],
    "advanced_heavy_battery_3":[],
    "improved_heavy_battery_4":[],
    "advanced_heavy_battery_4":[],
    "improved_heavy_battery_5":[],
    "advanced_heavy_battery_5":[]
}
for module in submarine_turrets:
    if BICE:
        gun_selecor(module,subGunTechs_set_BICE)
    else:
        gun_selecor(module,subGunTechs_set)

sub_tech_name = ""
sub_mergedTech_set = {}
sub_techEvents = []
if BICE:
    for key1,val1 in subGunTechs_set_BICE.items():
        for guns in val1:
            sub_tech_name = ("%s_submarine_turret"%key1)
            if sub_tech_name in sub_mergedTech_set:
                sub_mergedTech_set[copy.deepcopy(sub_tech_name)].append(copy.deepcopy(guns.name))
            else:
                sub_mergedTech_set[copy.deepcopy(sub_tech_name)] = [copy.deepcopy(guns.name)]
                eventStuf = DefTechEvents()
                eventStuf.name = copy.deepcopy(sub_tech_name)
                eventStuf.gunTech = copy.deepcopy(key1)
                if guns.caliber >=8:
                    #print("\n\t%s"%guns)
                    eventStuf.treatyCompliant = False
                sub_techEvents.append(eventStuf)
else:
    for key1,val1 in subGunTechs_set.items():
        for guns in val1:
            sub_tech_name = ("%s_submarine_turret"%key1)
            if sub_tech_name in sub_mergedTech_set:
                sub_mergedTech_set[copy.deepcopy(sub_tech_name)].append(copy.deepcopy(guns.name))
            else:
                sub_mergedTech_set[copy.deepcopy(sub_tech_name)] = [copy.deepcopy(guns.name)]
                eventStuf = DefTechEvents()
                eventStuf.name = copy.deepcopy(sub_tech_name)
                eventStuf.gunTech = copy.deepcopy(key1)
                sub_techEvents.append(eventStuf)
i=0

Tech_outputer(sub_mergedTech_set, "Output\\technologies\\Lic_MtG_Naval_Submarine_Turrets.txt")
Event_outputer(sub_techEvents, "Output\\events\\Lic_Submarine_Turrets_Events.txt", "Lic_submarine_turrets", "lic_tech_sub")
#local_ship_modules(submarine_turrets, "Output\\localisation\\english\\Lic_Submarine_Turrets_modules_l_english.yml")
local_tech(sub_mergedTech_set, "Output\\localisation\\english\\Lic_Submarine_Turrets_tech_l_english.yml")

#local_ship_modules_ger(merged_hybrid_array, "Output\\localisation\\german\\Lic_Hybrid_modules_l_german.yml")
#local_ship_modules_ger(submarine_turrets, "Output\\localisation\\german\\Lic_Submarine_Turrets_modules_l_german.yml")
#local_ship_modules_cn(merged_hybrid_array, "Output\\localisation\\chinese\\Lic_Hybrid_modules_l_cn.yml")
#local_ship_modules_cn(submarine_turrets, "Output\\localisation\\chinese\\Lic_Submarine_Turrets_modules_l_cn.yml")

gun_tech_list = ["basic_battery", "improved_light_battery_2", "advanced_light_battery_2", "improved_dp_light_battery_2", "advanced_dp_light_battery_2", "improved_medium_battery", "advanced_medium_battery", "modern_medium_battery", "improved_dp_medium_battery", "advanced_dp_medium_battery", "modern_dp_medium_battery", "basic_medium_battery_2", "improved_medium_battery_2", "advanced_medium_battery_2", "modern_medium_battery_2", "improved_heavy_battery", "advanced_heavy_battery", "basic_heavy_battery_2", "improved_heavy_battery_2", "advanced_heavy_battery_2", "basic_heavy_battery_3", "improved_heavy_battery_3", "advanced_heavy_battery_3", "improved_heavy_battery_4", "advanced_heavy_battery_4", "improved_heavy_battery_5", "advanced_heavy_battery_5"]
hanger_tech_list = ["converted", "armored"]
launcher_tech_list = ["small", "medium", "large"]

local_tech_ger(mergedTech_set, "Output\\localisation\\german\\Lic_Hybrid_tech_l_german.yml",gun_tech_list,hanger_tech_list,launcher_tech_list)
local_tech_ger(sub_mergedTech_set, "Output\\localisation\\german\\Lic_Submarine_Turrets_tech_l_german.yml",gun_tech_list,hanger_tech_list,launcher_tech_list)
#local_tech_cn(mergedTech_set, "Output\\localisation\\chinese\\Lic_Hybrid_tech_l_cn.yml",gun_tech_list,hanger_tech_list,launcher_tech_list)
#local_tech_cn(sub_mergedTech_set, "Output\\localisation\\chinese\\Lic_Submarine_Turrets_tech_l_cn.yml",gun_tech_list,hanger_tech_list,launcher_tech_list)

#top_view_hybrid(merged_hybrid_array, "Output\\_top view\\Lic_topview_capital_hybrid_rear.txt")
#top_view_hybrid(merged_hybrid_array, "Output\\_top view\\Lic_topview_cruiser_hybrid_rear.txt")


#Full gun module set
#capital
capital_gun_view_complete = []
capital_gun_view_front = []
capital_gun_view_rear = []
x=0
for cal in range(11,21):
    if cal == 17 or cal == 19:
        pass
    else:
        for GunPerTur in range(2,5):
            for TurNum in range(1,5):
                if (GunPerTur > 2 and TurNum > 3) or (GunPerTur > 3 and TurNum > 2):
                    pass
                else:
                    GunView = DefModule()
                    GunView.caliber = cal
                    GunView.numberGuns = GunPerTur * TurNum
                    GunView.numberTurrets = TurNum
                    GunView.category = "nrm_capital_battery_" + str(cal) + "_" + str(GunPerTur) + "x" + str(TurNum)
                    if not(TurNum > 3):
                        capital_gun_view_front.append(GunView)
                    capital_gun_view_rear.append(GunView)
                    capital_gun_view_complete.append(GunView)
                    x+=1
                    #print(GunView.category)
        #create a3x1_2x1 and a4x1_2x1
        GunView = DefModule()
        GunView.caliber = cal
        GunView.numberGuns = 5
        GunView.numberTurrets = 2
        GunView.category = "nrm_capital_battery_" + str(cal) + "_3x1_2x1"
        capital_gun_view_complete.append(GunView)
        capital_gun_view_front.append(GunView)
        capital_gun_view_rear.append(GunView)
        
        GunView = DefModule()
        GunView.caliber = cal
        GunView.numberGuns = 6
        GunView.numberTurrets = 2
        GunView.category = "nrm_capital_battery_" + str(cal) + "_4x1_2x1"
        capital_gun_view_complete.append(GunView)
        capital_gun_view_front.append(GunView)
        capital_gun_view_rear.append(GunView)
        x+=1
        #print(GunView.category)

#Cruiser
cruiser_gun_view_complete = []
cruiser_gun_view_front = []
cruiser_gun_view_rear = []
for cal in range(5,9):
    if cal == 7:
        pass
    else:
        for NumGuns in range(2,10):
            if not(NumGuns%2 == 0 or NumGuns%3 == 0 or NumGuns == 5) or NumGuns ==8:
                pass
            else:
                GunView = DefModule()
                GunView.caliber = cal
                GunView.numberGuns = NumGuns
                GunView.category = "nrm_cruiser_battery_" + str(cal) + "_x0" + str(NumGuns)
                cruiser_gun_view_complete.append(GunView)
                cruiser_gun_view_front.append(GunView)
                if not (NumGuns == 9):
                    cruiser_gun_view_rear.append(GunView)
                #print(GunView.category)
                x+=1
                if cal < 7: #Dual Purpse
                    GunView = DefModule()
                    GunView.caliber = cal
                    GunView.numberGuns = NumGuns
                    GunView.category = "nrm_cruiser_battery_DP_" + str(cal) + "_x0" + str(NumGuns)
                    cruiser_gun_view_complete.append(GunView)
                    cruiser_gun_view_front.append(GunView)
                    if not (NumGuns == 9):
                        cruiser_gun_view_rear.append(GunView)
                    #print(GunView.category)
                    x+=1
                if cal ==5: #5.5in
                    GunView = DefModule()
                    GunView.caliber = cal
                    GunView.numberGuns = NumGuns
                    GunView.category = "nrm_cruiser_battery_" + str(cal) + "h_x0" + str(NumGuns)
                    cruiser_gun_view_complete.append(GunView)
                    cruiser_gun_view_front.append(GunView)
                    if not (NumGuns == 9):
                        cruiser_gun_view_rear.append(GunView)
                    #print(GunView.category)
                    x+=1
                    GunView = DefModule()
                    GunView.caliber = cal
                    GunView.numberGuns = NumGuns
                    GunView.category = "nrm_cruiser_battery_DP_" + str(cal) + "h_x0" + str(NumGuns)
                    cruiser_gun_view_complete.append(GunView)
                    cruiser_gun_view_front.append(GunView)
                    if not (NumGuns == 9):
                        cruiser_gun_view_rear.append(GunView)
                    #print(GunView.category)
                    x+=1
i=0

for cal in range(10,13):
    for GunPerTur in range(2,5):
        for TurNum in range(1,3):
            if GunPerTur == 4 and TurNum ==2:
                pass
            else:
                GunView = DefModule()
                GunView.caliber = cal
                GunView.numberGuns = GunPerTur * TurNum
                GunView.numberTurrets = TurNum
                GunView.category = "nrm_cruiser_battery_PB_" + str(cal) + "_" + str(GunPerTur) + "x" + str(TurNum)
                cruiser_gun_view_complete.append(GunView)
                cruiser_gun_view_front.append(GunView)
                cruiser_gun_view_rear.append(GunView)
                x+=1
                #print(GunView.category)
print("%i gun top views"%x)

Module_deckgun_outputer(submarine_deckguns_x2, "Output\\modules\\Lic_sub_deckgun_x2.txt")

capital_gun_batteries_array_2x2 += capital_gun_batteries_array_Xx1_2x1
capital_gun_batteries_array_2x2 += capital_gun_batteries_array_singles
Module_Guns_outputer(capital_gun_batteries_array_2x2, "Output\\modules\\Lic_capital_battery.txt")
#local_ship_modules(capital_gun_batteries_array_2x2, "Output\\localisation\\english\\Lic_Capital_Battery_l_english.yml")


Module_Guns_outputer(cruiser_gun_batteries_array_temp, "Output\\modules\\Lic_cruiser_battery.txt")
#local_ship_modules(cruiser_gun_batteries_array_temp, "Output\\localisation\\english\\Lic_Cruiser_Battery_l_english.yml")

sub_conningtower_front = []
sub_conningtower_rear = []
sub_fantail = []
sub_used_modules = []
for module in submarine_turrets:
    if not module.category in sub_used_modules:
        sub_used_modules.append(module.category)
        if module.caliber >10:
            sub_conningtower_front.append(module)
        if module.caliber <10:
            sub_conningtower_front.append(module)
            sub_conningtower_rear.append(module)
        if module.caliber <6 and module.numberGuns <4:
            sub_fantail.append(module)
    pass
for module in submarine_deck_gun_array:
    if not module.category in sub_used_modules:
        sub_used_modules.append(module.category)
        sub_conningtower_front.append(module)
        sub_conningtower_rear.append(module)
        sub_fantail.append(module)
    pass
for module in submarine_deckguns_x2:
    if not module.category in sub_used_modules:
        sub_used_modules.append(module.category)
        sub_conningtower_front.append(module)
        sub_conningtower_rear.append(module)
    pass


top_view_guns(capital_gun_view_front,capital_gun_view_rear,"Output\\_top view\\Lic_topview_capital_.txt", capital_hybrid_array)
top_view_guns(cruiser_gun_view_front,cruiser_gun_view_rear,"Output\\_top view\\Lic_topview_crusier_.txt", cruiser_hybrid_array)
top_view_subs(sub_conningtower_front,sub_conningtower_rear,sub_fantail,"Output\\_top view\\Lic_topview_submarine_.txt")

fullModlueList = capital_gun_batteries_array_2x2 + merged_hybrid_array + submarine_turrets + cruiser_gun_batteries_array_temp + submarine_deckguns_x2
local_ship_modules_local(fullModlueList, "Output\\localisation\\english\\Lic_module_l_english.yml")
local_ship_modules_local_ger(fullModlueList, "Output\\localisation\\german\\Lic_module_l_german.yml")

print("%i Heavy Gun modues"%len(capital_gun_batteries_array_2x2))
print("%i Cruiser Gun modues"%len(cruiser_gun_batteries_array_temp))
print("%i Submarine Gun Batteries"%len(submarine_turrets))

#GetModuleData()
print(len(capital_gun_batteries_array))

