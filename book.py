import requests
import datetime
from bs4 import BeautifulSoup
import time

username = ''
password = ''
desiredTimeSlots = [1,2] #choose between 1, 2, 3 and 4 (max 2, separate with comma)
desiredSeatLocation = 'left' #choose between left, middle and right



rawURL = 'https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php'
currentDay = datetime.datetime.now().day
currentMonth = datetime.datetime.now().month
currentYear = datetime.datetime.now().year
currentHour = datetime.datetime.now().hour
currentMinute = datetime.datetime.now().minute
currentSecond = datetime.datetime.now().second


params = '?year=' + str(currentYear) + '&month=' + str(currentMonth) + '&day=' + str(currentDay) + '&area=42&room=702'

completeURL = rawURL + params
traget = 'day.php' + params
url = 'https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/admin.php'


formData = {
    'NewUserName': username,
    'NewUserPassword': password,
    'returl': completeURL,
    'TargetURL': traget,
    'Action': 'SetName'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

session = requests.Session()
response1 = session.post(url, data=formData, headers=headers)

print(response1.cookies)

response2 = session.get(completeURL, headers=headers)

print(response2.cookies)

def getSeats(response):
    soup = BeautifulSoup(response2.text, 'html.parser')

    #find table with id day_main
    table = soup.find('table', attrs={'id': 'day_main'})

    #find tbody in table
    tbody = table.find('tbody')

    #find all rows in table
    rows = tbody.find_all('tr')

    seats = []

    for row in rows:
        seatRow = []
        cells = row.find_all('td')
        cellLength = len(cells)
        for cell in cells:
    #get the class of the cell
            cellClass = cell.get('class')
            if 'new' in cellClass:
                seatRow.append(0)
            else:
                seatRow.append(1)

        seats.append(seatRow)
    return seats

def printSeatsMatrix(seats):
    for row in seats:
        print(row)

def findDesiredSeat(seats):
    seatLength = len(seats[0]) - 1
    if desiredSeatLocation == 'left':
        for i in range(seatLength, 0, -1):
            if checkTimeSlots(i) == False:
                continue #checks if seat is free for the desired time slots
            else:
                return i
        return i
    if desiredSeatLocation == 'right':
        for i in range(seatLength):
            if checkTimeSlots(i) == False:
                continue
            else:
                return i
        return i
    if desiredSeatLocation == 'middle':
        halfSeatLength = int(seatLength / 2)
        counter1 = 1
        counter2 = 1
        firstRound = True
        ticker = True
        while counter2 <= halfSeatLength + 2:

            if ticker == True and firstRound == False:
                i = halfSeatLength + counter1
                counter1 += 1
                ticker = False
            elif ticker == False and firstRound == False:
                i = halfSeatLength - counter2
                counter2 += 1
                ticker = True
            else:
                i = halfSeatLength
                firstRound = False
 
            if i not in range(seatLength):
                continue
            if checkTimeSlots(i) == False:
                continue
            return i


def checkTimeSlots(seatPosition):
    for i in range(len(desiredTimeSlots)):
        desiredTimeSlot = desiredTimeSlots[i] - 1
        if seats[desiredTimeSlot][seatPosition] != 0:
            return False
    return True
            
def bookSeat(seatPosition):
    roomIds = [698, 1164, 699, 1065, 700, 1166, 701, 1167, 702, 1168, 703, 1169, 704, 1170, 705, 1171, 706, 1172, 707, 1173, 708, 1174, 709, 1362]
    seconds = [43200, 43260, 43320, 43380]
    timeSlotsIds = ['vormittags+', 'nachmittags+', 'abends+', 'nachts+']
    second = currentHour * 3600 + currentMinute * 60 + currentSecond
    correctRoomId = roomIds[seatPosition - 1]

    print(correctRoomId)

    for i in range(len(desiredTimeSlots)):
        correctTimeSlot = timeSlotsIds[desiredTimeSlots[i] - 1]
        correctSeconds = seconds[desiredTimeSlots[i] - 1]


        request1Url = 'https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/edit_entry.php?area=42&room='+ str(correctRoomId) +'&period='+ str(desiredTimeSlots[i] - 1) +'&year='+ str(currentYear) +'&month='+ str(currentMonth) +'&day=' + str(currentDay)

        requestAjaxUrl = 'https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/edit_entry_handler.php'

        request2Url = 'https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/edit_entry_handler.php'

        returnURL = 'https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/day.php?year='+ str(currentYear) +'&month='+ str(currentMonth) +'&day='+ str(currentDay) +'&area=42&room='+ str(correctRoomId)

        formDataAjax = {
            'ajax': '1',
            'name': username,
            'description': correctTimeSlot,
            'start_day' : currentDay,
            'start_month' : currentMonth,
            'start_year' : currentYear,
            'start_seconds' : correctSeconds,
            'end_day' : currentDay,
            'end_month' : currentMonth,
            'end_year' : currentYear,
            'end_seconds' : correctSeconds,
            'area' : 42,
            'rooms[]' : correctRoomId,
            'type' : 'K',
            'confirmed' : 1,
            'returl' : "",
            'create_by' : username,
            'rep_id' : 0,
            'edit_type' : 'series'
        }

        ajaxHeaders = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        formData = {
            'name': username,
            'description': correctTimeSlot,
            'start_day' : currentDay,
            'start_month' : currentMonth,
            'start_year' : currentYear,
            'start_seconds' : correctSeconds,
            'end_day' : currentDay,
            'end_month' : currentMonth,
            'end_year' : currentYear,
            'end_seconds' : correctSeconds,
            'area' : 42,
            'rooms[]' : correctRoomId,
            'type' : 'K',
            'confirmed' : 1,
            'confirmed' : 1,
            'returl' : returnURL,
            'create_by' : username,
            'rep_id' : 0,
            'edit_type' : 'series'
        }

        response = session.get(request1Url, headers=ajaxHeaders)

        print(formDataAjax)

        responseAjax = session.post(requestAjaxUrl, data=formDataAjax, headers=headers)

        ajaxText = responseAjax.text

        if ajaxText != '{"valid_booking":true,"rules_broken":[],"conflicts":[]}':
            print("error")
            print(ajaxText)
            return False

        response1 = session.post(request2Url, data=formData, headers=headers)

        response2 = session.get(returnURL, headers=headers)

        time.sleep(1)

    return True




seats = getSeats(response2)

printSeatsMatrix(seats)

seat = findDesiredSeat(seats)

print(seat)

result = bookSeat(seat)

if result:
    print("")
    print("your seat has been booked")
    print("you can now go to the following link to look at your booking:")
    print("https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung")