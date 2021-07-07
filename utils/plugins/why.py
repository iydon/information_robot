from random import choice, choices


class why:
    special_case = (
        'the devil made me do it.', 'the computer did it.',
        'the customer is always right.', 'don''t you have something better to do?',
        'how should I know?', 'can you rephrase that?', 'it should be obvious.',
        'in the beginning, God created the heavens and the earth...',
        'why not?', 'don''t ask!', 'it''s your karma.', 'stupid question!',
    )
    preposition = ('of', 'from')
    proper_noun = (
        'Cleve', 'Jack', 'Bill', 'Joe', 'Pete', 'Loren', 'Damian',
        'Barney', 'Nausheen', 'Mary Ann', 'Penny', 'Mara',
    )
    noun = (
        'mathematician', 'programmer', 'system manager', 'engineer', 'hamster', 'kid',
    )
    nominative_pronoun = ('I', 'you', 'he', 'she', 'they')
    accusative_pronoun = ('me', 'all', 'her', 'him')
    nouned_verb = ('love', 'approval')
    adverb = ('very', 'not very', 'not excessively')
    adjective = (
        'tall', 'bald', 'young', 'smart', 'rich', 'terrified', 'good',
    )
    article = ('the', 'some', 'a')
    present_verb = ('fool', 'please', 'satisfy')
    transitive_verb = 6*('obeyed', ) + ('threatened', 'told', 'asked', 'helped')
    intransitive_verb = (
        'insisted on it', 'suggested it', 'told me to', 'wanted it',
        'knew it was a good idea', 'wanted it that way',
    )

    def __new__(cls):
        sw = {
            lambda: choice(cls.special_case): 1,
            cls.phrase: 3, cls.sentence: 6,
        }
        return choices(tuple(sw), weights=sw.values(), k=1)[0]().capitalize()

    @classmethod
    def phrase(cls):
        sw = (
            f'for the {choice(cls.nouned_verb)} {cls.prepositional_phrase()}.',
            f'to {choice(cls.present_verb)} {cls.object()}.',
            f'because {cls.sentence()}',
        )
        return choice(sw)

    @classmethod
    def prepositional_phrase(cls):
        sw = (
            f'{choice(cls.preposition)} {choice(cls.article)} {cls.noun_phrase()}',
            f'{choice(cls.preposition)} {choice(cls.proper_noun)}',
            f'{choice(cls.preposition)} {choice(cls.accusative_pronoun)}',
        )
        return choice(sw)

    @classmethod
    def sentence(cls):
        return f'{cls.subject()} {cls.predicate()}.'

    @classmethod
    def subject(cls):
        sw = {
            lambda: choice(cls.proper_noun): 1,
            lambda: choice(cls.nominative_pronoun): 1,
            lambda: f'{choice(cls.article)} {cls.noun_phrase()}': 2,
        }
        return choices(tuple(sw), weights=sw.values(), k=1)[0]()

    @classmethod
    def noun_phrase(cls):
        sw = {
            lambda: choice(cls.noun): 1,
            lambda: f'{cls.adjective_phrase()} {cls.noun_phrase()}': 1,
            lambda: f'{cls.adjective_phrase()} {choice(cls.noun)}': 2,
        }
        return choices(tuple(sw), weights=sw.values(), k=1)[0]()

    @classmethod
    def adjective_phrase(cls):
        sw = {
            lambda: choice(cls.adjective): 3,
            lambda: f'{cls.adjective_phrase()} and {cls.adjective_phrase()}': 2,
            lambda: f'{choice(cls.adverb)} {choice(cls.adjective)}': 1
        }
        return choices(tuple(sw), weights=sw.values(), k=1)[0]()

    @classmethod
    def predicate(cls):
        sw = {
            lambda: f'{choice(cls.transitive_verb)} {cls.object()}': 1,
            lambda: choice(cls.intransitive_verb): 2,
        }
        return choices(tuple(sw), weights=sw.values(), k=1)[0]()

    @classmethod
    def object(cls):
        sw = {
            lambda: choice(cls.accusative_pronoun): 1,
            lambda: f'{choice(cls.article)} {cls.noun_phrase()}': 9,
        }
        return choices(tuple(sw), weights=sw.values(), k=1)[0]()


print(why())
