{% test is_greater_than(model, column_name, value) %}

    select *
    from {{ model }}
    where {{ column_name }} <= {{ value }}

{% endtest %}

{% test is_greater_than_or_equal_to(model, column_name, value) %}

    select *
    from {{ model }}
    where {{ column_name }} < {{ value }}

{% endtest %}

{% test is_between(model, column_name, min_value, max_value) %}

    select *
    from {{ model }}
    where {{ column_name }} < {{ min_value }}
       or {{ column_name }} > {{ max_value }}

{% endtest %}

{% test is_valid_email(model, column_name) %}

    select *
    from {{ model }}
    where not regexp_matches({{ column_name }}, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')

{% endtest %}

{% test is_greater_than_or_equal_to_column(model, column_name, compare_to_column) %}

    select *
    from {{ model }}
    where {{ column_name }} < {{ compare_to_column }}

{% endtest %}
