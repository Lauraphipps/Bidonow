__all__ = ['register_test_case', 'assertPartial', 'TestCaseMixin', 'VERSION', 'AssertItem', 'assertExists', 'assertDoesNotExist']


VERSION = '1.0.0'


def register_test_case(test_case):
    test_case.addTypeEqualityFunc(AssertDict, get_assert_func(test_case, assert_assert_dict))
    test_case.addTypeEqualityFunc(AssertList, get_assert_func(test_case, assert_assert_list))


def assertPartial(test_case, real, expected):
    test_case.assertEqual(create(real), create(expected))


class TestCaseMixin(object):
    def __init__(self, *args, **kwargs):
        super(TestCaseMixin, self).__init__(*args, **kwargs)
        register_test_case(self)

    def assertPartial(self, real, expected):
        assertPartial(self, real, expected)


def create(value):
    if isinstance(value, dict):
        return AssertDict(value)
    if isinstance(value, list):
        return AssertList(value)
    return value


class AssertDict(dict):
    def __init__(self, base_dict, *args, **kwargs):
        super(AssertDict, self).__init__(*args, **kwargs)
        for key, value in base_dict.items():
            self[key] = create(value)


class AssertList(list):
    def __init__(self, base_list, *args, **kwargs):
        super(AssertList, self).__init__(*args, **kwargs)
        for item in base_list:
            self.append(create(item))


def get_assert_func(test_case, func):
    def wrapper(*args, **kwargs):
        return func(test_case, *args, **kwargs)
    return wrapper


def assert_assert_dict(test_case, real, expected, msg=None):
    for key, expected_value in expected.items():
        real_val = real.get(key)
        if isinstance(expected_value, AssertItem):
            expected_value.assert_item(real, key, test_case=test_case)
            continue

        if callable(expected_value):
            expected_value(real_val)
            continue

        if key not in real:
            raise AssertionError('Can not find key: {} in real dict'.format(key))

        test_case.assertEqual(real_val, expected_value)


def assert_assert_list(test_case, real, expected, msg=None):
    for idx, value in enumerate(expected):
        if len(real) <= idx:
            raise AssertionError('Can not find element with idx: {} in real list'.format(idx))
        real_val = real[idx]
        test_case.assertEqual(real_val, value)


class AssertItem(object):
    def assert_item(self, data, key, test_case):
        raise NotImplementedError()


class assertExists(AssertItem):
    def assert_item(self, data, key, test_case):
        if key not in data:
            raise AssertionError('Key {} does not exist in data {}'.format(key, data))


class assertDoesNotExist(AssertItem):
    def assert_item(self, data, key, test_case):
        if key in data:
            raise AssertionError('Key {} exists in data {}'.format(key, data))
