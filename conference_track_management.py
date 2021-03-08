

def covert_minute_to_hour(minute):
    """

    :param minute: get minute
    :return: hour:minute
    """
    hour = minute // 60
    minutes = minute % 60

    return "%d:%02d" % (hour, minutes)


class Track:

    def __init__(self):
        self.talk_track = []
        self.all_talk_list = Track.extract_input_to_dict()

    @staticmethod
    def extract_input_to_dict():
        """
        get data from txt file
        :return:  convert track talks to dictionary
        """
        talk_dict = {}
        try:
            with open('track.txt') as f:
                line_list = [line.strip() for line in f]
        except FileNotFoundError as e:
            print('File Not Found', e)
        for line in line_list:
            title, minutes = line.rsplit(maxsplit=1)
            try:
                minutes = int(minutes[:-3])
            # negative indexing raises error, so it means it's lightning
            except ValueError:
                minutes = 5
            talk_dict[line] = minutes
        return talk_dict

    def get_talks(self, start_talk, end_talk, session_shift):
        '''

        :param start_talk: start session time
        :param end_talk: end session time
        :param session_shift: session shift
        :return: all possible combination on the session shift
        '''
        new_dict = {}

        for title, time in list(sorted(self.all_talk_list.items())):
            session_duration = start_talk + time
            if session_duration <= end_talk:
                new_dict[str(covert_minute_to_hour(start_talk)) + session_shift] = title
                start_talk += time
                self.all_talk_list.pop(title)

        return new_dict

    def get_all_possible_track(self):
        """

        :return: get all the combination
        """

        track_id = 1
        while len(self.all_talk_list) != 0:
            talk_session = dict()
            talk_session["Track " + str(track_id)] = ":-"
            morning_shift = self.get_talks(540, 720, 'AM')
            talk_session.update(morning_shift)
            talk_session["12:00PM"] = 'Lunch'
            evening_shift = self.get_talks(60, 300, 'PM')
            talk_session.update(evening_shift)
            talk_session["5:00PM"] = 'Networking Event'
            self.talk_track.append(talk_session)
            track_id += 1

    def get_output(self):
        """

        :return: print all the track
        """
        for talk_obj in self.talk_track:
            for time, title in talk_obj.items():
                print(time, '-', title)

            print("\n")


if __name__ == '__main__':
    a = Track()
    a.get_all_possible_track()
    a.get_output()
