from dto import UserRegisterDTO


def check_validators(dto: UserRegisterDTO):
    assert dto.username, 'DTO not found'
    assert dto.username, 'Username is required'
    assert dto.password, 'Password is required'
