import axios, { AxiosError, type AxiosProgressEvent } from 'axios';
import { PUBLIC_API_LOCATION } from '$env/static/public';

const http = axios.create({
	baseURL: PUBLIC_API_LOCATION
});

export const predict = async (
	data: {
		videoHand: number;
		dominantHand: number;
		age: number;
		sex: number;
		file: File;
	},
	onUploadProgress: (e: AxiosProgressEvent) => void
) => {
	const formData = new FormData();
	formData.append('video_hand', data.videoHand.toString());
	formData.append('dominant_hand', data.dominantHand.toString());
	formData.append('age', data.age.toString());
	formData.append('sex', data.sex.toString());
	formData.append('video', data.file);

	try {
		const response = await http.post('/predict', formData, {
			headers: {
				'Content-Type': 'multipart/form-data'
			},
			onUploadProgress: onUploadProgress
		});

		return response.data;
	} catch (error: any) {
		return error.response || {};
	}
};

export const read_users = async () => {
	try {
		const response = await http.get('/users/', {
			headers: { accept: 'application/json', Authorization: `Bearer ${localStorage.getItem("token")}` }
		});
		return response.data;
	} catch (error) {
		return [];
	}
};

export const get_current_user = async () => {
	try {
		const response = await http.get('/users/current', {
			headers: { accept: 'application/json', Authorization: `Bearer ${localStorage.getItem("token")}` }
		});
		return response.data;
	} catch (error) {
		return null;
	}
};

export const token_login = async (username: string, password: string) => {
	const data = new FormData();
	data.append('username', username);
	data.append('password', password);

	try {
		const response = await http.post('/token', data);
		return response.data;
	} catch (error) {
		return null;
	}
};

export const create_user = async (username: string, password: string) => {
	try {
		const response = await http.post('/users/', { username, password }, { headers: { accept: 'application/json', Authorization: `Bearer ${localStorage.getItem("token")}` } });
		return response.data;
	} catch (error) {
		return null;
	}
}

export const delete_user = async (user_id: number) => {
	try {
		const response = await http.delete(`/users/${user_id}`, { headers: { accept: 'application/json', Authorization: `Bearer ${localStorage.getItem("token")}` } });
		return response.data;
	} catch (error) {
		return null;
	}
}

export const read_models = async () => {
	try {
		const response = await http.get('/models/', {
			headers: { accept: 'application/json', Authorization: `Bearer ${localStorage.getItem("token")}` }
		});
		return response.data;
	} catch (error) {
		return [];
	}
};

export const add_model = async (
	name: string,
	model: File
) => {
	const formData = new FormData();
	formData.append('name', name);
	formData.append('model', model);

	try {
		const response = await http.post('/models/', formData, {
			headers: {
				'Content-Type': 'multipart/form-data',
				'Authorization': `Bearer ${localStorage.getItem("token")}`
			},
		});

		return response.data;
	} catch (error: any) {
		return null;
	}
}

export const delete_model = async (model_id: number) => {
	try {
		const response = await http.delete(`/models/${model_id}`, { headers: { accept: 'application/json', Authorization: `Bearer ${localStorage.getItem("token")}` } });
		return response.data;
	} catch (error) {
		return null;
	}
}

export const select_model = async (model_id: number) => {
	const formData = new FormData();
	formData.append('model_id', model_id.toString());
	try {
		const response = await http.post(`/select_model`, formData, { headers: { accept: 'application/json', Authorization: `Bearer ${localStorage.getItem("token")}` } });
		return response.data;
	} catch (error) {
		return null;
	}
}