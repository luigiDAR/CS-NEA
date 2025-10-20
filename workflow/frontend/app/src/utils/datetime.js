export function getDBformatDate(jsDate){
    //Converting from JS date format, to MariaDB date
    const dateObj = new Date(jsDate)
    const firstFormat = `${dateObj.getFullYear()}-${dateObj.getMonth()+1}-${dateObj.getDate()} ${dateObj.getHours()}:${dateObj.getMinutes()}:${dateObj.getSeconds()}`

    //Splitting the full string into smaller arrays
    const dateTimeArray = firstFormat.split(/\s+/);
    const dateArray = dateTimeArray[0].split("-")
    const timeArray = dateTimeArray[1].split(":")

    //Adding leading zero's
    if (dateArray[1].length==1){
        dateArray[1] = "0"+dateArray[1]
    }
    if (dateArray[2].length==1){
        dateArray[2] = "0"+dateArray[2]
    }

    for (let i=0;i<3;i++){
        if(timeArray[i].length==1){
            timeArray[i] = "0"+timeArray[i]
        }
    }

    //Adding the smaller arrays back into the full string
    const dateString = dateArray.join("-")
    const timeString = timeArray.join(":")
    const secondFormat = dateString.concat(" ",timeString);
    return secondFormat
}
