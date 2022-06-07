import random
import re
import string

import pytest

from src.handy import re_pattern


class TestRePattern:
    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            (string.printable, []),
            ('纯中文', ['纯', '中', '文']),
            (f'中{string.printable}文', ['中', '文']),
        ),
    )
    def test_chinese_character(
        self,
        s: str,
        expected: list[str],
    ):
        p = re.compile(re_pattern.CN_CHAR)
        assert p.findall(s) == expected

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('abc', False),
            ('123', False),
            ('!@#', False),
            ('abc123', False),
            ('abc!@#', False),
            ('123!@#', False),
            ('abc123!@#', False),
            ('abc.', False),
            ('123.', False),
            ('!@#.', False),
            ('abc123.', False),
            ('abc!@#.', False),
            ('123!@#.', False),
            ('abc123!@#.', False),
            ('abc..', False),
            ('123..', False),
            ('!@#..', False),
            ('abc123..', False),
            ('abc!@#..', False),
            ('123!@#..', False),
            ('abc123!@#..', False),
            ('abc.d', False),
            ('123.d', False),
            ('abc123.d', False),
            ('abc.dd', True),
            ('123.dd', True),
            ('abc123.dd', True),
            ('abc.ddd', True),
            ('123.ddd', True),
            ('abc123.ddd', True),
            ('a.ddd', True),
            ('a.1', False),
            ('a.12', False),
            ('a.123', False),
            ('a.1a', False),
            ('a.a1', False),
            ('a.a1b', False),
            ('a.ab', True),
            ('-abc.org', False),
            ('abc-.org', False),
            ('a-bc.org', True),
            ('a-b-c.org', True),
            ('a-b-c.-org', False),
            ('a-b-c.o-rg', False),
            ('a-b-c.org-', False),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, 1024),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(string.ascii_letters, k=random.randint(2, 1024))
                ),
                True,
            ),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, 1024),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits + '-',
                        k=random.randint(1, 1024),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, 1024),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(string.ascii_letters, k=random.randint(2, 1024))
                ),
                True,
            ),
        ),
    )
    def test_domain_name_en(self, s: str, expected: bool):
        p = re.compile(
            re_pattern.DOMAIN_NAMES[re_pattern.LANGUAGE.EN][0] + r'$', re.IGNORECASE
        )
        m = p.match(s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('纯中文', False),
            ('abc', False),
            ('123', False),
            ('abc中文', False),
            ('123中文', False),
            ('纯中文.', False),
            ('abc.', False),
            ('123.', False),
            ('中文abc.', False),
            ('中文123.', False),
            ('纯中文..', False),
            ('abc..', False),
            ('123..', False),
            ('中文abc..', False),
            ('中文123..', False),
            ('纯中文.d', False),
            ('abc.d', False),
            ('123.d', False),
            ('中文abc.d', False),
            ('中文123.d', False),
            ('纯中文.dd', True),
            ('abc.dd', False),
            ('123.dd', False),
            ('中文abc.dd', True),
            ('中文123.ddd', True),
            ('纯中文.ab', True),
            ('纯中文.中文', True),
            ('中文abc.ab', True),
            ('中文abc.中文', True),
            ('中文abc.a中文', False),
            ('纯中文.a中文', False),
            ('abc.a中文', False),
            ('-中文.org', False),
            ('中文-.org', False),
            ('a-中文.org', True),
            ('a-中文-c.org', True),
            ('a-中文-c.-org', False),
            ('a-中文-c.o-rg', False),
            ('a-中文-c.org-', False),
            ('-中文.中文', False),
            ('中文-.中文', False),
            ('a-中文.中文', True),
            ('a-中文-c.中文', True),
            ('a-中文-c.-中文', False),
            ('a-中文-c.中-文', False),
            ('a-中文-c.中文-', False),
            # (
            #     ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + '.'
            #     + ''.join(
            #         random.choices(string.ascii_letters, k=random.randint(2, 1024))
            #     ),
            #     True,
            # ),
            # (
            #     ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + '.'
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             ), k=random.randint(2, 1024))
            #     ),
            #     True,
            # ),
            # (
            #     ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits
            #             + '-',
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + '.'
            #     + ''.join(
            #         random.choices(string.ascii_letters, k=random.randint(2, 1024))
            #     ),
            #     True,
            # ),
            # (
            #     ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits
            #             + '-',
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + '.'
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             ),
            #             k=random.randint(2, 1024),
            #         )
            #     ),
            #     True,
            # ),
        ),
    )
    def test_domain_name_cn(self, s: str, expected: bool):
        p = re.compile(
            re_pattern.DOMAIN_NAMES[re_pattern.LANGUAGE.CN][0] + r'$', re.IGNORECASE
        )
        m = p.match(s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None