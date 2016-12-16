package main

import (
	"errors"
	"log"
	"strconv"

	"golang.org/x/net/context"

	"grpc.sample/kv"
	"grpc.sample/search"
)

type KvService struct {
	values map[string]string
}

func (s *KvService) SetValue(ctx context.Context, in *kv.SetValueRequest) (*kv.SetValueResponse, error) {
	s.values[in.Key] = in.Value
	panic("test")
	//return &kv.SetValueResponse{Result: kv.SetValueResponse_SUCC}, nil
	return nil, errors.New("test")
}

func (s *KvService) GetValue(ctx context.Context, in *kv.GetValueRequest) (*kv.GetValueResponse, error) {
	if v, ok := s.values[in.Key]; ok {
		return &kv.GetValueResponse{Result: kv.GetValueResponse_Found, Value: v}, nil
	}

	return &kv.GetValueResponse{Result: kv.GetValueResponse_NotFound, Value: ""}, nil
}

type SearchService struct{}

func (s *SearchService) Search(ctx context.Context, in *search.SearchRequest) (*search.SearchResponse, error) {
	log.Println("------ Search(Golang)")
	panic("test")
	var response = new(search.SearchResponse)
	for i := 0; i < int(in.ResultPerPage); i++ {
		var result = new(search.Result)
		result.Url = "localhost:50052/" + strconv.Itoa(int(in.PageNumber))
		result.Title = in.Query
		result.Snippets = append(result.Snippets, "xxxx")
		response.Results = append(response.Results, result)
	}
	return response, nil
}
