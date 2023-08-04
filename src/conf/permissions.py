from api_utils.access import PermissionRegistry


permissions = PermissionRegistry('common_pod_auth_pii', 10000, 11000)


# User API methods
PERMISSION__PII_GET_USER = permissions.add('PII_GET_USER', 1, 'get user', 'user')
PERMISSION__PII_GET_USERS_LIST = permissions.add('PII_GET_USERS_LIST', 2, 'get users list', 'user')
PERMISSION__PII_MOD_USER_DATA = permissions.add('PII_MOD_USER_DATA', 3, 'update user data', 'user')
PERMISSION__PII_DEL_USER = permissions.add('PII_DEL_USER', 4, 'delete user', 'user')
PERMISSION__PII_GET_USER_ORGANIZATIONS_LIST = permissions.add('PII_GET_USER_ORGANIZATIONS_LIST', 5, 'get user organizations list', 'user')
PERMISSION__PII_GET_USER_TEAMS_LIST = permissions.add('PII_GET_USER_TEAMS_LIST', 7, 'get user teams list', 'user')

# Organization API methods
PERMISSION__PII_GET_ORG = permissions.add('PII_GET_ORG', 8, 'get organization', 'organization')
PERMISSION__PII_GET_ORG_LIST = permissions.add('PII_GET_ORG_LIST', 9, 'get organizations list', 'organization')
PERMISSION__PII_GET_ORG_TPL = permissions.add('PII_GET_ORG_TPL', 10, 'get organization template', 'organization')
PERMISSION__PII_MK_ORG = permissions.add('PII_MK_ORG', 11, 'create organization', 'organization')
PERMISSION__PII_MOD_ORG = permissions.add('PII_MOD_ORG', 12, 'update organization', 'organization')
PERMISSION__PII_MOD_CURRENT_ORG = permissions.add('PII_MOD_CURRENT_ORG', 13, 'update current organization', 'organization')
PERMISSION__PII_DEL_ORG = permissions.add('PII_DEL_ORG', 14, 'delete organization', 'organization')
PERMISSION__PII_GET_ORG_USER = permissions.add('PII_GET_ORG_USER', 15, 'get organization user', 'organization')
PERMISSION__PII_GET_ORG_USERS_LIST = permissions.add('PII_GET_ORG_USERS_LIST', 16, 'get organization users list', 'organization')

# Team API methods
PERMISSION__PII_GET_ORG_TEAM = permissions.add('PII_GET_ORG_TEAM', 17, 'get organization team', 'team')
PERMISSION__PII_GET_ORG_TEAMS_LIST = permissions.add('PII_GET_ORG_TEAMS_LIST', 18, 'get organization teams list', 'team')
PERMISSION__PII_GET_ORG_TEAM_TPL = permissions.add('PII_GET_ORG_TEAM_TPL', 19, 'get new organization team template', 'team')
PERMISSION__PII_MK_ORG_TEAM = permissions.add('PII_MK_ORG_TEAM', 20, 'create new organization team', 'team')
PERMISSION__PII_MK_CURRENT_ORG_TEAM = permissions.add('PII_MK_CURRENT_ORG_TEAM', 21, 'create new organization team in current organization', 'team')
PERMISSION__PII_MOD_ORG_TEAM = permissions.add('PII_MOD_ORG_TEAM', 22, 'update organization team', 'team')
PERMISSION__PII_MOD_CURRENT_ORG_TEAM = permissions.add('PII_MOD_CURRENT_ORG_TEAM', 23, 'update organization team on current organization', 'team')
PERMISSION__PII_DEL_ORG_TEAM = permissions.add('PII_DEL_ORG_TEAM', 24, 'delete organization team', 'team')
PERMISSION__PII_DEL_CURRENT_ORG_TEAM = permissions.add('PII_DEL_CURRENT_ORG_TEAM', 25, 'delete organization team in current organization', 'team')

# Team users management API methods
PERMISSION__PII_GET_ORG_TEAM_USERS_LIST = permissions.add('PII_GET_ORG_TEAM_USERS_LIST', 26, 'get list of users in organization team ', 'team_managment')
PERMISSION__PII_ADD_USER_TO_ORG_TEAM = permissions.add('PII_ADD_USER_TO_ORG_TEAM', 27, 'add user to organization team', 'team_user')
PERMISSION__PII_ADD_USER_TO_CURRENT_ORG_TEAM = permissions.add('PII_ADD_USER_TO_CURRENT_ORG_TEAM', 28, 'add user to organization team in current organization', 'team_managment')
PERMISSION__PII_DEL_USER_FROM_ORG_TEAM = permissions.add('PII_DEL_USER_FROM_ORG_TEAM', 29, 'delete user from organization team', 'team_user')
PERMISSION__PII_DEL_USER_FROM_CURRENT_ORG_TEAM = permissions.add('PII_DEL_USER_FROM_CURRENT_ORG_TEAM', 30, 'delete user from current organization team', 'team_managment')

# Invite user API
PERMISSION__PII_GET_USER_INVITE = permissions.add('PII_GET_USER_INVITE', 31, 'get user credentials invite', 'invite')
PERMISSION__PII_GET_ORG_USER_INVITES_LIST = permissions.add('PII_GET_ORG_USER_INVITES_LIST', 32, 'get user credentials invites list on organization', 'invite')
PERMISSION__PII_GET_CURRENT_ORG_USER_INVITES_LIST = permissions.add('PII_GET_CURRENT_ORG_USER_INVITES_LIST', 33, 'get user credentials invites list on current organization', 'invite')
PERMISSION__PII_GET_USER_INVITE_TPL = permissions.add('PII_GET_USER_INVITE_TPL', 34, 'get invite template', 'invite')
PERMISSION__PII_MK_USER_INVITE_TO_ORG_TEAM = permissions.add('PII_MK_USER_INVITE_TO_ORG_TEAM', 35, 'create invite to organization', 'invite')
PERMISSION__PII_MK_USER_INVITE_TO_CURRENT_ORG_TEAM = permissions.add('PII_MK_USER_INVITE_TO_CURRENT_ORG_TEAM', 36, 'create invite to current organization ', 'invite')
PERMISSION__PII_DEL_USER_INVITE = permissions.add('PII_DEL_USER_INVITE', 37, 'delete invite', 'invite')


DEFAULT_ORGANIZATION_AVAILABLE_PERMISSION_LIST = [
    PERMISSION__PII_MOD_CURRENT_ORG,
    PERMISSION__PII_GET_ORG_TEAM_TPL,
    PERMISSION__PII_MK_CURRENT_ORG_TEAM,
    PERMISSION__PII_MOD_CURRENT_ORG_TEAM,
    PERMISSION__PII_DEL_CURRENT_ORG_TEAM,
    PERMISSION__PII_ADD_USER_TO_CURRENT_ORG_TEAM,
    PERMISSION__PII_DEL_USER_FROM_CURRENT_ORG_TEAM,
    PERMISSION__PII_GET_CURRENT_ORG_USER_INVITES_LIST,
    PERMISSION__PII_MK_USER_INVITE_TO_CURRENT_ORG_TEAM
]
