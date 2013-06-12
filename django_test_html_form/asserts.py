import unittest

from bs4 import BeautifulSoup


class AssertHtmlFormContext(unittest.TestCase):

    def __init__(self, response, form_name, action, method):
        self.response = response
        self.form_name = form_name
        self.action = action
        self.method = method

    def parse_content(self):
        return BeautifulSoup(self.response.content)

    def form(self, html):
        search = {}
        if self.form_name:
            search = {'name': self.form_name}
        form = html.find('form', search)

        if not form:
            err = "Couldn't find any form on the page."
            if self.form_name:
                err = (
                    "Couldn't find form with name %s on the page."
                    % self.form_name
                )
            self.fail(err)

        if form['method'].lower() != self.method.lower():
            self.fail(
                "The form method %s is different than %s."
                % (form['method'], self.method)
            )

        if self.action is not None and form['action'] != self.action:
            self.fail(
                "The form action %s is different than %s."
                % (form['action'], self.action)
            )

    def extract_fields(self, form):
        """
        Turn a BeautifulSoup form in to a dict of fields and default values
        """
        fields = {}
        for input in form.findAll('input'):
            # ignore submit/image with no name attribute
            if input['type'] in (
                'submit', 'image'
            ) and not input.has_key('name'):
                continue

            # single element nome/value fields
            if input['type'] in (
                'text', 'hidden', 'password', 'submit', 'image'
            ):
                value = ''
                if input.has_key('value'):
                    value = input['value']
                fields[input['name']] = value
                continue

            # checkboxes and radios
            if input['type'] in ('checkbox', 'radio'):
                value = ''
                if input.has_key('checked'):
                    if input.has_key('value'):
                        value = input['value']
                    else:
                        value = 'on'
                if fields.has_key(input['name']) and value:
                    fields[input['name']] = value

                if not fields.has_key(input['name']):
                    fields[input['name']] = value

                continue

            self.fail("Input type %s not supported" % input['type'])

        # textareas
        for textarea in form.findAll('textarea'):
            fields[textarea['name']] = textarea.string or ''

        # select fields
        for select in form.findAll('select'):
            value = ''
            options = select.findAll('option')
            is_multiple = select.has_key('multiple')
            selected_options = [
                option for option in options
                if option.has_key('selected')
            ]

            # If no select options, go with the first one
            if not selected_options and options:
                selected_options = [options[0]]

            if not is_multiple:
                assert(len(selected_options) < 2)
                if len(selected_options) == 1:
                    value = selected_options[0]['value']
            else:
                value = [option['value'] for option in selected_options]

            fields[select['name']] = value

        return fields

    def __enter__(self):
        html = self.parse_content()
        form = self.form(html)
        fields = self.extract_fields(form)
        return {'form': form, 'fields': fields}

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def assertHtmlForm(self,
                       response,
                       form_name=None,
                       action=None,
                       method='POST'):
        context = AssertHtmlFormContext(response, form_name, action, method)
        return context
