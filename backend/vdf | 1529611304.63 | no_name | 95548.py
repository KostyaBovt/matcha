
        select *
        from users_interests
        inner join interests
        on users_interests.interest_id = interests.id
        where users_interests.user_id='100'
    