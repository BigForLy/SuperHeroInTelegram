import requests
import const


class SendManager:

    def __init__(self, hero_manager, bot, chat_id):
        for one_hero in hero_manager.heroes:
            text_message = '<b>' + one_hero.name + '</b>' + '\n' + \
                           '<pre>Biography</pre>' + '\n' + \
                           'Full name: ' + one_hero.full_name + '\n' + \
                           'Alter egos: ' + one_hero.alter_egos + '\n' + \
                           'Aliases: ' + one_hero.aliases + '\n' + \
                           'Place of birth: ' + one_hero.aliases + '\n' + \
                           'First appearance: ' + one_hero.first_appearance + '\n' + \
                           'Publisher: ' + one_hero.publisher + '\n' + \
                           '<pre>Appearance</pre>' + '\n' + \
                           'Gender: ' + one_hero.gender + '\n' + \
                           'Race: ' + one_hero.race + '\n' + \
                           'Height: ' + one_hero.height + '\n' + \
                           'Weight: ' + one_hero.weight + '\n' + \
                           'Eye color: ' + one_hero.eye_color + '\n' + \
                           'Hair color: ' + one_hero.hair_color + '\n' + \
                           '<pre>Work</pre>' + '\n' + \
                           'Occupation: ' + one_hero.occupation + '\n' + \
                           'Base: ' + one_hero.base + '\n' + \
                           '<pre>Connections</pre>' + '\n' + \
                           'Group affiliation: ' + one_hero.group_affiliation + '\n' + \
                           'Relatives: ' + one_hero.relatives + '\n'
            bot.send_photo(chat_id, one_hero.image, caption=text_message, parse_mode='HTML')


class HeroManager:

    def __init__(self, heroes_name):
        self.__session = requests.Session()
        self.hero_selected = False
        self.hero_count = 0
        self.error = None
        self.heroes = []
        self.__get_hero_by_name(heroes_name)

    def __get_hero_by_name(self, heroes_name):
        res = self.__session.get(const.url + '/search/' + heroes_name)
        try:
            if res.status_code != 200:
                self.error = 'Please try again later'
                raise Exception
            elif res.json()['response'] != 'success':
                self.error = res.json()['error'].capitalize()
                raise Exception
            hero_list = res.json()['results']
            for one_hero in hero_list:
                self.hero_selected = True
                self.hero_count += 1
                self.heroes.append(Hero(one_hero, self.__session))
        except Exception as ex:
            print(ex)


class Appearance(object):
    def __init__(self, one_hero):
        super().__init__(one_hero)
        self.__appearance = one_hero['appearance']
        self.gender = self.__appearance['gender']
        self.race = self.__appearance['race']
        self.height = ' / '.join(str(i) for i in (self.__appearance['height']))
        self.weight = ' / '.join(str(i) for i in (self.__appearance['weight']))
        self.eye_color = self.__appearance['eye-color']
        self.hair_color = self.__appearance['hair-color']


class Biography(object):
    def __init__(self, one_hero):
        super().__init__(one_hero)
        self.__biography = one_hero['biography']
        self.full_name = self.__biography['full-name']
        self.alter_egos = self.__biography['alter-egos']
        self.aliases = ', '.join(str(i) for i in (self.__biography['aliases']))
        self.place_of_birth = self.__biography['place-of-birth']
        self.first_appearance = self.__biography['first-appearance']
        self.publisher = self.__biography['publisher']


class Connections(object):
    def __init__(self, one_hero):
        super().__init__(one_hero)
        self.__connections = one_hero['connections']
        self.relatives = self.__connections['relatives']
        self.group_affiliation = self.__connections['group-affiliation']


class Work(object):
    def __init__(self, one_hero):
        self.__connections = one_hero['work']
        self.occupation = self.__connections['occupation']
        self.base = self.__connections['base']


class Hero(Appearance, Biography, Connections, Work):
    def __init__(self, one_hero, sess):
        super().__init__(one_hero)
        self.id = one_hero['id']
        self.name = one_hero['name']
        self.image = self.load_image(sess, one_hero['image']['url'])

    @staticmethod
    def load_image(sess, url):
        r = sess.get(url)
        if r.status_code == 200:
            return r.content
        else:
            return None
