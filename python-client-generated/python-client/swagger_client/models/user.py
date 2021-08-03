# coding: utf-8

"""
    Event Management System

    This YAML doc depicts the various endpoints to a RESTapi for a Event management system  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: apiteam@swagger.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from swagger_client.configuration import Configuration


class User(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'full_name': 'str',
        'email': 'str',
        'password': 'str',
        'profile_photo': 'str',
        'role': 'str',
        'created_at': 'date'
    }

    attribute_map = {
        'id': 'id',
        'full_name': 'full_name',
        'email': 'email',
        'password': 'password',
        'profile_photo': 'profile_photo',
        'role': 'role',
        'created_at': 'created_at'
    }

    def __init__(self, id=None, full_name=None, email=None, password=None, profile_photo=None, role=None, created_at=None, _configuration=None):  # noqa: E501
        """User - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._full_name = None
        self._email = None
        self._password = None
        self._profile_photo = None
        self._role = None
        self._created_at = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if full_name is not None:
            self.full_name = full_name
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password
        if profile_photo is not None:
            self.profile_photo = profile_photo
        if role is not None:
            self.role = role
        if created_at is not None:
            self.created_at = created_at

    @property
    def id(self):
        """Gets the id of this User.  # noqa: E501


        :return: The id of this User.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this User.


        :param id: The id of this User.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def full_name(self):
        """Gets the full_name of this User.  # noqa: E501


        :return: The full_name of this User.  # noqa: E501
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """Sets the full_name of this User.


        :param full_name: The full_name of this User.  # noqa: E501
        :type: str
        """

        self._full_name = full_name

    @property
    def email(self):
        """Gets the email of this User.  # noqa: E501


        :return: The email of this User.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this User.


        :param email: The email of this User.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def password(self):
        """Gets the password of this User.  # noqa: E501


        :return: The password of this User.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this User.


        :param password: The password of this User.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def profile_photo(self):
        """Gets the profile_photo of this User.  # noqa: E501


        :return: The profile_photo of this User.  # noqa: E501
        :rtype: str
        """
        return self._profile_photo

    @profile_photo.setter
    def profile_photo(self, profile_photo):
        """Sets the profile_photo of this User.


        :param profile_photo: The profile_photo of this User.  # noqa: E501
        :type: str
        """

        self._profile_photo = profile_photo

    @property
    def role(self):
        """Gets the role of this User.  # noqa: E501


        :return: The role of this User.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this User.


        :param role: The role of this User.  # noqa: E501
        :type: str
        """
        allowed_values = ["admin", "user"]  # noqa: E501
        if (self._configuration.client_side_validation and
                role not in allowed_values):
            raise ValueError(
                "Invalid value for `role` ({0}), must be one of {1}"  # noqa: E501
                .format(role, allowed_values)
            )

        self._role = role

    @property
    def created_at(self):
        """Gets the created_at of this User.  # noqa: E501


        :return: The created_at of this User.  # noqa: E501
        :rtype: date
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this User.


        :param created_at: The created_at of this User.  # noqa: E501
        :type: date
        """

        self._created_at = created_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(User, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, User):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, User):
            return True

        return self.to_dict() != other.to_dict()