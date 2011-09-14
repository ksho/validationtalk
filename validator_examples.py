"""
Some examples of basic validators
"""
# Bool
>>> from formencode import validators as v
>>> v.Bool.to_python(0)
False
>>> v.Bool.to_python(True)
True
>>> v.Bool.to_python(None)
False
>>> v.Bool.to_python('')
False

# Strings
>>> v.String().to_python('I\'d be crazy not to follow')
"I'd be crazy not to follow"
>>> v.String(max=10).to_python('Follow where you lead')
Traceback (most recent call last):
  ...
formencode.api.Invalid: Enter a value less than 10 characters long
>>> v.String(max=10).to_python('Your eyes')
'Your eyes'

# Dates
>>> d = v.DateValidator(earliest_date=datetime(2009, 4, 22))
>>> d.to_python(datetime(2010, 7, 11))
datetime.datetime(2010, 7, 11, 0, 0)
>>> d.to_python(datetime(2005, 7, 11))
Traceback (most recent call last):
  ...
formencode.api.Invalid: Date must be after Wednesday, 22 April 2009

# Email addresses
>>> v.Email().to_python('karl@monetate.com')
'karl@monetate.com'
>>> v.Email().to_python('karlmonetate')
Traceback (most recent call last):
  ...
formencode.api.Invalid: An email address must contain a single @

"""
Example schema for form
"""
class UserForm(formencode.schema.Schema):
    """
    Validates some form elements.
    """
    first_name = validators.String(not_empty=True)
    last_name = validators.String(not_empty=True)
    email = validators.Email()
    username = validators.String(not_empty=True)

# Call to UserForm schema
validators.UserForm.to_python(
    {
    'first_name': 'karl',
    'last_name': 'shouler',
    'username': 'kmano8',
    'email': 'karl@monetate.com'
    })

"""
Example password custom validator
"""
class SecurePassword(validators.FancyValidator):

    def validate_python(self, value, state):
        if len(value) < 8:
            raise formencode.Invalid('Your password must be at least 8 characters',
                value, state)
        non_letters = self.LETTER_REGEX.sub('', value)
        if len(non_letters) < self.REQ_NON_LETTER:
            raise formencode.Invalid(
                self.message('Your password requires at least 1 non-alpha character',
                value, state)

# Example schema for a password form
class PasswordForm(formencode.schema.Schema):
    """
    Validates password fields
    """
    new_password = SecurePassword(not_empty=False)
    new_password_again = validators.String(not_empty=False)
    chained_validators = [validators.FieldsMatch(
        'new_password', 'new_password_again')]

