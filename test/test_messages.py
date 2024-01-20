import pytest
from app.models import schema


def test_get_all_messages(authorized_client, test_messages):
    res = authorized_client.get("/message/")

    def validate(message):
        return schema.MessageResponse(**message)
    messages_map = map(validate, res.json())
    posts_list = list(messages_map)

    assert len(res.json()) == len(test_messages)
    assert res.status_code == 200



def test_unauthorized_user_get_message(client):
    res = client.get(f"/message/")
    assert res.status_code == 401


def test_message_action_not_exist(authorized_client):
    res = authorized_client.put(f"/message/88888?action=wrongaction")
    assert res.status_code == 400



@pytest.mark.parametrize("message_content, context, receivers", [
    ("awesome new message", "awesome new context", [1]),
    ("favorite Food", "Delivered", [1]),
    ("travel plan", "app notify", [1]),
])
def test_publish_message(authorized_client, message_content, context, receivers):
    res = authorized_client.post(
        "/message/", json={"message_content": message_content, "context": context, "receivers": receivers})

    # created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert res.json().get('message') == 'Messages published successfully'

def test_unauthorized_publish_message(client, test_user, test_messages):
    res = client.post(
        "/message/", json={"message_content": "message_content", "context": "context", "receivers": [1]})
    assert res.status_code == 401



def test_mark_message_unknown_user(authorized_client):
    res = authorized_client.put(
        f"/message/1?action=seen")

    assert res.status_code == 404

def test_mark_message_with_wrong_action(authorized_client):
    res = authorized_client.put(
        f"/message/1?action=wrongaction")

    assert res.status_code == 400

