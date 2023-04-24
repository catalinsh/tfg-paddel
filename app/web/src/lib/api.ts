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

	const response = await http.post('/predict', formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		},
		onUploadProgress: onUploadProgress
	});

	return response.data;
};

export const read_users = async (token: string) => {
	try {
		const response = await http.get('/users/', {
			headers: { accept: 'application/json', Authorization: `Bearer ${token}` }
		});
		return response.data;
	} catch (error) {
		return [];
	}
};

export const get_current_user = async (token: string) => {
	try {
		const response = await http.get('/users/current', {
			headers: { accept: 'application/json', Authorization: `Bearer ${token}` }
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
