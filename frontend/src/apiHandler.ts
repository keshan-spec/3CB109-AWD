// import axios from 'axios';

const BASE_URI = 'http://localhost:5010/api/v1';

// const client = axios.create({
//     baseURL: BASE_URI,
//     json: true,
// });

class APIClient {
    accessToken: string;

    constructor(accessToken: string) {
        this.accessToken = accessToken;
    }

    login(email: string, password: string) {
        return fetch('http://localhost:5010/api/v1/login', {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password
            })
        })
    }

    // createKudo(repo) {
    //     return this.perform('post', '/kudos', repo);
    // }

    // deleteKudo(repo) {
    //     return this.perform('delete', `/kudos/${repo.id}`);
    // }

    // getKudos() {
    //     return this.perform('get', '/kudos');
    // }

    // async perform(method, resource, data=null) {
    //     return client({
    //         method,
    //         url: resource,
    //         data,
    //         headers: {
    //             Authorization: `Bearer ${this.accessToken}`
    //         }
    //     }).then(resp => {
    //         return resp.data ? resp.data : [];
    //     })
    // }
}

export default APIClient;