import os.path

from sorl.thumbnail import ImageField

from django.db import models
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractBaseUser

from mycv.apps.accounts.managers import MyCVUserManager


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    for backend in auth.get_backends():
        if hasattr(backend, "has_perm"):
            if backend.has_perm(user, perm, obj):
                return True
    return False


def _user_has_module_perms(user, app_label):
    for backend in auth.get_backends():
        if hasattr(backend, "has_module_perms"):
            if backend.has_module_perms(user, app_label):
                return True
    return False


class MyCVUser(AbstractBaseUser):

    def determine_path(instance, filename):
        return os.path.join(u'uploads', u'avatars', unicode(instance.id), unicode(filename))

    # User Profile
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    #permissions
    is_superuser = models.BooleanField(_('superuser status'), default=False,
                                       help_text=_('Designates that this user has all permissions without '
                                                   'explicitly assigning them.'))
    groups = models.ManyToManyField(Group, verbose_name=_('groups'),
                                    blank=True, help_text=_('The groups this user belongs to. A user will '
                                                            'get all permissions granted to each of '
                                                            'his/her group.'),
                                    related_name="users", related_query_name="applicant")
    user_permissions = models.ManyToManyField(Permission,
                                              verbose_name=_('user permissions'), blank=True,
                                              help_text=_('Specific permissions for this user.'),
                                              related_name="users", related_query_name="applicant")

    avatar = ImageField(max_length=255, upload_to=determine_path, null=True, blank=True)
    address = models.ForeignKey("core.Address", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyCVUserManager()

    def __unicode__(self):
        return "%s's" % self.screen_name

    class Meta:
        verbose_name = _("Applicant Profile")
        verbose_name_plural = _("Applicant profiles")

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('accounts:user_profile', [str(self.id)])

    @property
    def screen_name(self):
        #First name and last name are required
        first = self.first_name or ''
        if first and len(first) > 1:
            first = first[0].upper() + first[1:]
        last = self.last_name or ''
        if last:
            if len(last) > 1:
                last = last[0].upper() + last[1:]
                last = "%s." % last[0]
            else:
                last = last[0]
        if first or last:
            return u"%s %s" % (first, last)
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Returns the short name for the user."""
        return self.first_name


    #permissions related methods
    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through his/her
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


