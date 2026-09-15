package com.example.movieticketbooking.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "admins")
public class Admin extends User {

    @Column(name = "department", length = 50)
    private String department;

    @Column(name = "admin_level")
    private Integer adminLevel = 1;

    public Admin() {
        super();
        this.setRole(Role.ROLE_ADMIN);
    }

    public Admin(String username, String email, String password, String fullName, String phone, String department) {
        super(username, email, password, fullName, phone, Role.ROLE_ADMIN);
        this.department = department;
        this.adminLevel = 1;
    }

    @Override
    public String getDisplayRole() {
        return "System Administrator (" + (department != null ? department : "Operations") + ")";
    }

    @Override
    public int getMaxAllowedBookingsPerDay() {
        return 1000;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public Integer getAdminLevel() {
        return adminLevel;
    }

    public void setAdminLevel(Integer adminLevel) {
        this.adminLevel = adminLevel;
    }
}
