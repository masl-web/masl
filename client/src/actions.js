export const addBrand = (payload) => {
    return {
      type: 'ADD_BRAND',
      payload,
    };
};

export const removeBrand = (payload) => {
    return {
      type: 'REMOVE_BRAND',
      payload,
    };
};

export const setAddress = (payload) => {
    return {
      type: "SET_ADDRESS",
      payload,
    }
}

export const setLocation = (payload) => {
  return {
    type: "SET_LOCATION",
    payload,
  }
}
