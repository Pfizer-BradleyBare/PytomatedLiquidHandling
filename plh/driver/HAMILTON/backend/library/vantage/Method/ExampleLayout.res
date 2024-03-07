#pragma once
global resource Res_TrackGripper(1, 0xff0000, Translate("TrackGripper"));
global resource Res_EntryExit(1, 0xff0000, Translate("EntryExit"));
global resource Res_ML_STAR(1, 0xff0000, Translate("ML_STAR"));


function Res_TrackGripper_map(variable unit) variable { return(unit); }
function Res_TrackGripper_rmap(variable address) variable { return(address); }

function Res_EntryExit_map(variable unit) variable { return(unit); }
function Res_EntryExit_rmap(variable address) variable { return(address); }

function Res_ML_STAR_map(variable unit) variable { return(unit); }
function Res_ML_STAR_rmap(variable address) variable { return(address); }


namespace ResourceUnit {
     variable Res_TrackGripper;
     variable Res_EntryExit;
     variable Res_ML_STAR;
}
// $$author=FCNCHV-ARDLC$$valid=0$$time=2024-03-07 12:15$$checksum=ece99e55$$length=089$$