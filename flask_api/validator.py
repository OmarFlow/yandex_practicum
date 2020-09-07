def create_error_msg(field, error, error_type):
    return {
      "detail": [
        {
          "loc": [
            "query",
            field
          ],
          "msg": error,
          "type": error_type
        }
      ]
    }


def validator(data):
    for int_param in ['limit', 'page']:
        try:
            int(data.get(int_param))
        except ValueError as e:
            return create_error_msg(int_param, 'Value is not valid integer', type(e).__name__)

    if data.get('sort') not in {'id', 'title', 'imdb_rating', ''}:
        return create_error_msg(
            'sort',
            'Invalid value for sort try id, title or imdb_rating',
            'ValueError'
        )

    if data.get('sort_order') not in {'asc', 'desc', ''}:
        return create_error_msg(
            'sort_order',
            'Invalid value for sort_order try asc, desc',
            'ValueError'
        )