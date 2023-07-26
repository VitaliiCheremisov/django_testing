class TestsUrls:
    ANONYMOUS = (
        'notes:home',
        'users:login',
        'users:logout',
        'users:signup'
    )
    AUTHS = (
        'notes:list',
        'notes:add',
        'notes:success'
    )
    AVAILAIBLE_DIFF_USERS = (
        'notes:detail',
        'notes:edit',
        'notes:delete'
    )
    REDIRECTS_WITH_SLUG = (
        'notes:detail',
        'notes:edit',
        'notes:delete'
    )
    REDIRECTS_WITHOUT_SLUG = (
        'notes:list',
        'notes:add',
        'notes:success'
    )
