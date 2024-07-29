const hoverMap = {
    'FarmerJobGrid'  : 'FarmerJobToolTip',
    'HuntersJobGrid' : 'HuntersJobToolTip',
    'CooksJobGrid' : 'CooksJobToolTip',
    'LoggersJobGrid' : 'LoggersJobToolTip',
    'ButchersJobGrid' : 'ButchersJobToolTip',
    'BuilderJobGrid' : "BuildersJobToolTip"

}


function toggleHover() {
    const tab = document.getElementById(hoverMap[this.id]); //.style.visibility = "visible";
    tab.style.visibility = 'visible';
 }

 function toggleHoverOff() {
    const tab = document.getElementById(hoverMap[this.id]); //.style.visibility = "visible";
    tab.style.visibility = 'hidden';
 }

