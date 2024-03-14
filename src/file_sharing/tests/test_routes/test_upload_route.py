
async def test_post_upload_route(client, fixture_give_upload_file):
    data = {'file': open('src/file_sharing/tests/test.txt', 'rb')}
    response = await client.post('/files', files=data)
    response_json = response.json()
    print(response_json)
    assert response.status_code == 201

