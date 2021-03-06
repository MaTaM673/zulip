from typing import Dict, Any

from zerver.lib.test_classes import ZulipTestCase

from zerver.lib.validator import check_widget_content

class WidgetContentTestCase(ZulipTestCase):
    def test_validation(self) -> None:
        def assert_error(obj: object, msg: str) -> None:
            self.assertEqual(check_widget_content(obj), msg)

        assert_error(5,
                     'widget_content is not a dict')

        assert_error({},
                     'widget_type is not in widget_content')

        assert_error(dict(widget_type='whatever'),
                     'extra_data is not in widget_content')

        assert_error(dict(widget_type='zform', extra_data=4),
                     'extra_data is not a dict')

        assert_error(dict(widget_type='bogus', extra_data={}),
                     'unknown widget type: bogus')

        extra_data = dict()  # type: Dict[str, Any]
        obj = dict(widget_type='zform', extra_data=extra_data)

        assert_error(obj, 'zform is missing type field')

        extra_data['type'] = 'bogus'
        assert_error(obj, 'unknown zform type: bogus')

        extra_data['type'] = 'choices'
        assert_error(obj, 'heading key is missing from extra_data')

        extra_data['heading'] = 'whatever'
        assert_error(obj, 'choices key is missing from extra_data')

        extra_data['choices'] = 99
        assert_error(obj, 'extra_data["choices"] is not a list')

        extra_data['choices'] = [99]
        assert_error(obj, 'extra_data["choices"][0] is not a dict')

        extra_data['choices'] = [
            dict(long_name='foo', reply='bar'),
        ]
        assert_error(obj, 'short_name key is missing from extra_data["choices"][0]')

        extra_data['choices'] = [
            dict(short_name='a', long_name='foo', reply='bar'),
        ]

        self.assertEqual(check_widget_content(obj), None)
