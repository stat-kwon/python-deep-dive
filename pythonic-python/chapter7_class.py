# 7.8 컴포지션을 통한 상속 피하기
class Stack(list):
    def push(self, item):
        self.append(item)


s = Stack()
s.push(1)
s.push(2)
s.push(3)
s.pop()
s.pop()


# 위 자료구조는 스택처럼 동작함과 동시에 list의 method까지 사용 가능하다. -> implementation inheritance(구현 상속)
# 실제 사용하고자 하는 method 이외에 불필요한 method까지 포함되는 문제점이 있다. -> 스택에 정렬 메서드가 있을 필요는 없음
# 더 나은 방법은 컴포지션(composition)이다.

class Stack:
    def __init__(self):
        self._items = list()

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def __len__(self):
        return len(self._items)


s = Stack()
s.push(1)
s.push(2)
s.push(3)
s.pop()
s.pop()


# 이전과 동일하지만 스택에만 초점을 맞춘 코드로 관련 없는 리스트 메서드나 스택 기능이 아닌 것들은 없다.
# 위 구현을 확장하여 내부 list 클래스를 추가 인수로 받을 수 있다.
class Stack:
    def __init__(self, container):
        if container is None:
            container = list()
        self._items = container

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def __len__(self):
        return len(self._items)


# 이 방식의 이점은 구성 요소들의 느슨한 결합(loosely coupling)을 촉진 한다는 것이다.
import array

s = Stack(container=array.array('i'))  # 의존성 주입의 예
s.push(42)
s.push(23)
# s.push('a lot')
# 의존성 주입 : 사용하는 객체가 아닌 외부의 독립적인 객체가 인스턴스를 생성한 후 이를 전달하여 의존성을 해결하는 방법


# 때때로 클래스 변수와 클래스 메서드를 같이 사용하여 인스턴스 동작 방식을 구성하고 제어하는 경우가 있다.
import time


class Date:
    datefmt = '{year}-{month:02d}-{day:02d}'

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return self.datefmt.format(year=self.year,
                                   month=self.month,
                                   day=self.day)

    @classmethod
    def from_timestamp(cls, ts):
        tm = time.localtime(ts)
        return cls(tm.tm_year, tm.tm_mon, tm.tm_mday)

    @classmethod
    def today(cls):
        return cls.from_timestamp(time.time())


class MDYDate(Date):
    datefmt = '{month}/{day}/{year}'


class DMYDate(Date):
    datefmt = '{day}/{month}/{year}'


a = Date(1967, 4, 9)
print(a)

b = MDYDate(1967, 4, 9)
print(b)

c = DMYDate(1967, 4, 9)
print(c)

print()
a = MDYDate.today()
b = DMYDate.today()
print(a)
print(b)
print(a.__dict__)
# 클래스 메서드는 인스턴스를 생성하는 다른 방법으로 사용하기도 한다.
# 클래스 메서드는 from_timestamp()처럼 from_과 같은 접두사를 사용하는 이름 규약을 따른다.

