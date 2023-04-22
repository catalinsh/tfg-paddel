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

	let result: object;

	await http
		.post('/predict', formData, {
			headers: {
				'Content-Type': 'multipart/form-data'
			},
			onUploadProgress: onUploadProgress
		})
		.then((r) => r.data)
		.then((data) => (result = { result: data }))
		.catch((e: AxiosError) => (result = { result: 'error', message: e.message }));

	return result!;
};

export const read_users = async (token: string) => {
	let result;

	await http
		.get('/users/', {
			headers: { accept: 'application/json', Authorization: `Bearer ${token}` }
		})
		.then((r) => r.data)
		.then((data) => (result = data))
		.catch((e: AxiosError) => (result = { result: 'error', message: e.message }));

	return result;
};
