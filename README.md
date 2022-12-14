
This python script can be used to automatically book a seat in the KIT library

## Warning

this was hacked together in a few hours - there are probably bugs

### Install

1.  install python 3.x

2. install bot via console
 
   ```shell
   $ cd {path/to/your/basefolder} 
   $ git clone https://github.com/trsommer/kitBookSeat.git
   $ pip install bs4 requests
   ```

3. add your credentials

   ```python
   username = "[your kit library username]"
   password = "[your kit library password"
   ```

4. configure where and when you want to book

   ```python
   desiredTimeSlots = [1,2] #choose between 1, 2, 3 and 4 (max 2, separate with comma)
   desiredSeatLocation = 'left' #choose between left, middle and right
   ```

	4.1 Timeslots
   - 08:00 to 13:00  => 1
   - 13:00 to 18:00 => 2
   - 18:00 to 22:00 => 3
   - 22:00 to 08:00  => 4

	4.2
  
	 - left: finds the closest seat that matches your time config starting from the left
	 - middle: finds the closest seat that matches your time config starting from the middle
	 - right: finds the closest seat that matches your time config starting from the right

### Run

   ```shell
   $ python book.py
   ```
