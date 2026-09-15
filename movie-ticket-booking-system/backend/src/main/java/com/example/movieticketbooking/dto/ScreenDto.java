package com.example.movieticketbooking.dto;

public class ScreenDto {
    private Long id;
    private String name;
    private Integer totalRows;
    private Integer totalColumns;
    private Long theatreId;
    private String theatreName;

    public ScreenDto() {}

    public ScreenDto(Long id, String name, Integer totalRows, Integer totalColumns, Long theatreId, String theatreName) {
        this.id = id;
        this.name = name;
        this.totalRows = totalRows;
        this.totalColumns = totalColumns;
        this.theatreId = theatreId;
        this.theatreName = theatreName;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getTotalRows() {
        return totalRows;
    }

    public void setTotalRows(Integer totalRows) {
        this.totalRows = totalRows;
    }

    public Integer getTotalColumns() {
        return totalColumns;
    }

    public void setTotalColumns(Integer totalColumns) {
        this.totalColumns = totalColumns;
    }

    public Long getTheatreId() {
        return theatreId;
    }

    public void setTheatreId(Long theatreId) {
        this.theatreId = theatreId;
    }

    public String getTheatreName() {
        return theatreName;
    }

    public void setTheatreName(String theatreName) {
        this.theatreName = theatreName;
    }
}
